#!/usr/bin/env python3
"""Regenerate the automatic sections of README.md from the GitHub API.

The README contains blocks delimited by
    <!-- AUTO:<name>:START --> ... <!-- AUTO:<name>:END -->
Only the content between the markers is replaced; everything else is yours.

Usage (in CI the token comes from GITHUB_TOKEN):
    python scripts/update_readme.py
    python scripts/update_readme.py --dry-run                 # print, don't write
    python scripts/update_readme.py --repos-json repos.json   # offline test
"""
import argparse
import html
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.github.com"


# --------------------------------------------------------------------------- API
def request(url):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "profile-readme-updater",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def fetch_repos(user):
    repos, page = [], 1
    while True:
        batch = request(f"{API}/users/{user}/repos?type=owner&per_page=100&page={page}")
        repos += batch
        if len(batch) < 100:
            return repos
        page += 1


def fetch_languages(user, name):
    try:
        return request(f"{API}/repos/{user}/{name}/languages")
    except Exception:
        return {}


def fetch_last_commit(user, name):
    try:
        c = request(f"{API}/repos/{user}/{name}/commits?per_page=1")[0]["commit"]
        return c["message"].splitlines()[0], c["author"]["date"]
    except Exception:  # empty repo, no access, rate limit...
        return None


# ---------------------------------------------------------------------- helpers
def esc(text, limit=None):
    text = " ".join((text or "").split())
    if limit and len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    return html.escape(text, quote=False).replace("|", "\\|")


def rel(iso):
    then = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    days = int((datetime.now(timezone.utc) - then).total_seconds() // 86400)
    if days < 1:
        return "today"
    if days == 1:
        return "yesterday"
    if days < 30:
        return f"{days} days ago"
    if days < 365:
        m = days // 30
        return f"{m} month{'s' if m > 1 else ''} ago"
    y = days // 365
    return f"{y} year{'s' if y > 1 else ''} ago"


def link(repo):
    return f"[{repo['name']}]({repo['html_url']})"


def category(repo, cfg):
    overrides = cfg.get("category_overrides") or {}
    if repo["name"] in overrides:
        return overrides[repo["name"]]
    topic_map = cfg.get("categories") or {}
    for topic in repo.get("topics") or []:
        if topic in topic_map:
            return topic_map[topic]
    return repo.get("language") or "Other"


def table(rows):
    out = ["| Project | Description | Stack | ★ | Last push |", "|---|---|---|--:|---|"]
    for r, tagline in rows:
        stack = r.get("language") or ""
        topics = [t for t in (r.get("topics") or []) if t != (stack or "").lower()][:3]
        tags = " ".join(f"`{t}`" for t in ([stack] if stack else []) + topics)
        out.append(
            f"| **{link(r)}** | {esc(tagline or r.get('description') or '—', 140)} | {tags} "
            f"| {r['stargazers_count'] or ''} | {rel(r['pushed_at'])} |"
        )
    return "\n".join(out)


# --------------------------------------------------------------------- sections
def section_featured(repos, cfg):
    by_name = {r["name"]: r for r in repos}
    chosen, used = [], set()
    for item in cfg.get("featured") or []:
        name = item["repo"] if isinstance(item, dict) else item
        if name in by_name and name not in used:
            chosen.append((by_name[name], item.get("tagline") if isinstance(item, dict) else None))
            used.add(name)
    slots = int(cfg.get("featured_slots") or 0)
    if len(chosen) < slots:
        pool = sorted(
            (r for r in repos if not r["fork"] and r["name"] not in used),
            key=lambda r: (r["stargazers_count"], r["pushed_at"]),
            reverse=True,
        )
        chosen += [(r, None) for r in pool[: slots - len(chosen)]]
    return table(chosen) if chosen else "_Nothing to show yet._"


def section_recent(repos, cfg, user, offline):
    own = [r for r in repos if not r["fork"]]
    own.sort(key=lambda r: r["pushed_at"], reverse=True)
    lines = []
    for r in own[: int(cfg.get("recent_count") or 5)]:
        commit = None if offline else fetch_last_commit(user, r["name"])
        if commit:
            msg, date = commit
            lines.append(f"- **{link(r)}** — {esc(msg, 90)} · _{rel(date)}_")
        else:
            lines.append(f"- **{link(r)}** · _{rel(r['pushed_at'])}_")
    return "\n".join(lines) or "_No recent activity._"


def section_projects(repos, cfg):
    groups = {}
    for r in repos:
        if not r["fork"]:
            groups.setdefault(category(r, cfg), []).append(r)
    if not groups:
        return "_No projects yet._"
    order = cfg.get("category_order") or []
    names = sorted(groups, key=lambda n: (n == "Other", order.index(n) if n in order else len(order), n.lower()))
    blocks = []
    for name in names:
        items = sorted(groups[name], key=lambda r: r["pushed_at"], reverse=True)
        blocks.append(
            f"<details open>\n<summary><b>{esc(name)}</b> ({len(items)})</summary>\n\n"
            + table([(r, None) for r in items])
            + "\n\n</details>"
        )
    return "\n\n".join(blocks)


def section_forks(repos, cfg):
    forks = sorted((r for r in repos if r["fork"]), key=lambda r: r["pushed_at"], reverse=True)
    if not (cfg.get("show_forks") and forks):
        return ""
    lines = [f"- {link(r)}" + (f" — {esc(r['description'], 100)}" if r.get("description") else "") for r in forks]
    return (
        f"<details>\n<summary><b>Forks &amp; contributions</b> ({len(forks)})</summary>\n\n"
        + "\n".join(lines)
        + "\n\n</details>"
    )


def section_stats(repos, cfg, user, offline):
    own = [r for r in repos if not r["fork"]]
    stars = sum(r["stargazers_count"] for r in own)
    head = f"**{len(own)}** projects · **{stars}** ★ received · **{len(repos) - len(own)}** forks"
    totals = {}
    for r in own:
        langs = {r["language"]: 1} if offline and r.get("language") else ({} if offline else fetch_languages(user, r["name"]))
        for lang, size in langs.items():
            totals[lang] = totals.get(lang, 0) + size
    if not totals:
        return head
    total = sum(totals.values())
    top = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)[: int(cfg.get("languages_top") or 6)]
    rows = []
    for lang, size in top:
        pct = size / total * 100
        filled = round(pct / 100 * 20)
        rows.append(f"{lang:<14}{'█' * filled}{'░' * (20 - filled)}  {pct:5.1f}%")
    return head + "\n\n```text\n" + "\n".join(rows) + "\n```"


# ------------------------------------------------------------------------- main
def replace_block(text, name, content):
    pattern = re.compile(rf"(<!-- AUTO:{name}:START -->)(.*?)(<!-- AUTO:{name}:END -->)", re.S)
    if not pattern.search(text):
        sys.exit(f"Marker block AUTO:{name} not found in README")
    body = f"\n{content}\n" if content else "\n"
    return pattern.sub(lambda m: m.group(1) + body + m.group(3), text, count=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--readme", default=str(ROOT / "README.md"))
    ap.add_argument("--config", default=str(ROOT / "config.yml"))
    ap.add_argument("--repos-json", help="read repos from a JSON file instead of the API (offline test)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8")) or {}
    user = cfg["username"]
    offline = bool(args.repos_json)

    repos = json.load(open(args.repos_json)) if offline else fetch_repos(user)
    hidden = set(cfg.get("exclude") or []) | {user}  # never list the profile repo itself
    repos = [
        r for r in repos
        if r["name"] not in hidden and not r.get("private") and (cfg.get("show_archived") or not r.get("archived"))
    ]

    readme = Path(args.readme)
    text = readme.read_text(encoding="utf-8")
    text = replace_block(text, "stats", section_stats(repos, cfg, user, offline))
    text = replace_block(text, "featured", section_featured(repos, cfg))
    text = replace_block(text, "recent", section_recent(repos, cfg, user, offline))
    text = replace_block(text, "projects", section_projects(repos, cfg))
    text = replace_block(text, "forks", section_forks(repos, cfg))
    text = replace_block(text, "meta", f"Auto-generated from my repositories · synced {datetime.now(timezone.utc):%Y-%m-%d}")

    if args.dry_run:
        print(text)
    else:
        readme.write_text(text, encoding="utf-8")
        print(f"README updated: {len(repos)} repos processed")


if __name__ == "__main__":
    main()
