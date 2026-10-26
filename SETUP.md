# Setup (10 minutes, one time)

How it works: every push in one of your repos triggers a small workflow that pings
your profile repo; the profile repo runs `scripts/update_readme.py`, which reads your
repositories through the GitHub API and rewrites the automatic sections of `README.md`.
A 6-hour schedule acts as a safety net (new repos, renames, stars).

## 1. Put the files in the profile repository

The profile repo is `andrei-borcea/andrei-borcea` (it must be public).
Copy into it, keeping the paths:

```
README.md
config.yml
SETUP.md                          (optional)
scripts/update_readme.py
scripts/install_notify.sh         (optional, see step 3)
snippets/notify-profile.yml       (optional, see step 3)
.github/workflows/update-readme.yml
```

Commit and push to `main`. In the repo go to **Actions → Update profile README → Run
workflow** to generate the sections for the first time. Check that the workflow has
write access: **Settings → Actions → General → Workflow permissions → Read and write**.

## 2. Create the token used by the other repos

The `GITHUB_TOKEN` of a repo cannot trigger workflows in another repo, so you need a
personal token that can only do that:

1. GitHub → Settings → Developer settings → Personal access tokens → **Fine-grained tokens**.
2. Repository access: **Only select repositories** → `andrei-borcea/andrei-borcea`.
3. Permissions → Repository → **Contents: Read and write** (this is what the
   `/dispatches` endpoint requires). Nothing else.
4. Set an expiration (e.g. 1 year) and add a calendar reminder to renew it. If it
   expires, nothing breaks: the 6-hour schedule keeps the README fresh.

## 3. Add the notify workflow to your repos

Automatic (all your own, non-fork, non-archived repos):

```bash
gh auth refresh -s workflow            # one time, to allow writing workflow files
export PROFILE_DISPATCH_TOKEN=github_pat_xxx
./scripts/install_notify.sh            # dry run, lists the repos
./scripts/install_notify.sh --apply    # does it
```

Manual, per repo: copy `snippets/notify-profile.yml` to `.github/workflows/` and add
the secret `PROFILE_DISPATCH_TOKEN` (Settings → Secrets and variables → Actions).
For new repos, repeat this step.

## 4. Customize

Everything lives in `config.yml`: featured projects (with optional custom taglines),
categories, hidden repos, forks, language bar. Pushing a change to `config.yml`
regenerates the README immediately. To group projects automatically, add **topics** to
your repos (e.g. `ai`, `devops`, `react-native`) matching the `categories` map.

Anything outside the `<!-- AUTO:... -->` markers in `README.md` (about, stack,
contacts) is yours to edit by hand and is never touched by the script.

## Notes

- Only **public** repositories are listed; private ones are never exposed.
- The relative dates ("3 days ago") make the README change daily, so you will see a
  bot commit about once a day. This also keeps the scheduled workflow from being
  disabled for inactivity.
- Local test without touching anything: `python scripts/update_readme.py --dry-run`
  (needs `pip install pyyaml`; without a token the API allows 60 requests/hour).
