<h1 align="center">Hi, I'm Andrei Borcea 👋</h1>
<h3 align="center">Systems & Performance Engineer · Reverse Engineering · On-Device AI · DevOps & Cloud</h3>

<p align="center">
  <a href="https://www.linkedin.com/in/andrei-borcea"><img src="https://img.shields.io/badge/LinkedIn-andrei--borcea-0A66C2?style=flat&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="https://t.me/hustlercoder"><img src="https://img.shields.io/badge/Telegram-@hustlercoder-26A5E4?style=flat&logo=telegram&logoColor=white" alt="Telegram"></a>
  <img src="https://img.shields.io/badge/Based_in-Italy-009246?style=flat" alt="Italy">
</p>

---

## 🧑‍💻 About Me

I'm a software engineer who likes to understand systems **all the way down** — from the bits of a quantized weight block to the flash controller's queue depth. My background spans **low-level C/C++**, **mobile platforms**, **cloud infrastructure** and **DevOps automation**, and lately I've been focused on making large language models run fast and privately **on phones**.

I'm passionate about **reverse engineering**: taking apart binaries, file formats, drivers and undocumented platform behaviour to learn how they really work — and then using that knowledge to build faster, more reliable software. I measure before I optimize, and I write down what didn't work as carefully as what did.

I'm always eager to learn, and I'm open to **collaborating on open-source projects**.

---

## 🔥 Featured Project

### [Liyab](https://github.com/andrei-borcea/liyab) — on-device LLM inference for Android & iOS

<a href="https://github.com/andrei-borcea/liyab"><img src="https://github.com/andrei-borcea/liyab/raw/main/docs/brand/liyab-mark.svg" width="72" align="right" alt="Liyab logo"></a>

A **C++20 GGUF inference engine** that runs open language models directly on phones, with no cloud dependency — including models **larger than the device's RAM**, streamed from flash storage.

- ⚡ **35B mixture-of-experts on a phone:** Qwen3.6-35B-A3B (22 GB) decodes at **~9 tok/s** on a Snapdragon 8 Elite within a 5.5 GB memory budget, by streaming experts from UFS with parallel `O_DIRECT` reads, an LFU expert cache and router-based prefetch of the next block's experts
- 🧮 **Every GGML tensor format** (F16/BF16, Q4–Q8, K-quants, I-quants, ternary, MXFP4/NVFP4), decoded **bit-exactly** against llama.cpp's reference, with hand-tuned **ARM NEON / SDOT / i8mm** kernels
- 🎮 **GPU backends:** Vulkan compute for Adreno/Mali (zero-copy reads from GPU-shared memory, 23 native formats, +25% decode vs CPU) and Metal on Apple
- 🌡️ **Power & thermal manager:** SoC detection (Snapdragon, Dimensity, Tensor, Exynos, Apple), token pacing and throttle-aware routing NPU → GPU → CPU
- 🧠 **Modern model support:** Llama, Mistral, Qwen2/3/3.5 incl. Gated DeltaNet hybrids and MoE, paged & quantized KV cache, sliding-window attention, speculative decoding
- 📱 **Liyab Chat**, a native Android demo app with Hugging Face model browser, resumable multi-connection downloads and a live performance overlay
- ✅ Stable C ABI with Kotlin/JNI and Swift bindings, self-contained test suites, every claim backed by on-device benchmarks

![C++20](https://img.shields.io/badge/C++20-00599C?style=flat&logo=cplusplus&logoColor=white)
![Vulkan](https://img.shields.io/badge/Vulkan-AC162C?style=flat&logo=vulkan&logoColor=white)
![Metal](https://img.shields.io/badge/Metal-000000?style=flat&logo=apple&logoColor=white)
![ARM NEON](https://img.shields.io/badge/ARM_NEON-0091BD?style=flat&logo=arm&logoColor=white)
![Android NDK](https://img.shields.io/badge/Android_NDK-3DDC84?style=flat&logo=android&logoColor=white)
![CMake](https://img.shields.io/badge/CMake-064F8C?style=flat&logo=cmake&logoColor=white)
![License](https://img.shields.io/badge/License-Apache_2.0-blue?style=flat)

---

## 🔍 Reverse Engineering & Low-Level Interests

- Binary and file-format analysis — understanding undocumented layouts byte by byte
- Android internals: SELinux policies, FUSE storage, vendor thermal sensors, OEM memory limits
- Mobile SoCs and accelerators: CPU micro-architecture, GPU drivers, NPU runtimes
- Performance profiling and memory/I-O behaviour of real hardware

<!-- TODO: add your reverse-engineering projects and tools here (e.g. Ghidra, IDA, Frida, radare2) -->

---

## 🧩 Other Projects & Contributions

<!-- TODO: add your other own projects here, one line each:
- **[project-name](https://github.com/andrei-borcea/project-name)** — short description · tech
-->

- Forks and contributions to **React Native**, **wa-automate-nodejs** (WhatsApp automation for Node.js) and jQuery plugins

---

## 🛠️ Tech Stack

**Languages**
![C](https://img.shields.io/badge/C-A8B9CC?style=flat&logo=c&logoColor=black)
![C++](https://img.shields.io/badge/C++-00599C?style=flat&logo=cplusplus&logoColor=white)
![Java](https://img.shields.io/badge/Java-ED8B00?style=flat&logo=openjdk&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![C#](https://img.shields.io/badge/C%23-512BD4?style=flat&logo=dotnet&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)

**Systems, GPU & Mobile**
![ARM NEON](https://img.shields.io/badge/ARM_NEON_/_SDOT_/_i8mm-0091BD?style=flat&logo=arm&logoColor=white)
![Vulkan](https://img.shields.io/badge/Vulkan_Compute-AC162C?style=flat&logo=vulkan&logoColor=white)
![Metal](https://img.shields.io/badge/Metal-000000?style=flat&logo=apple&logoColor=white)
![Android NDK](https://img.shields.io/badge/Android_NDK_/_JNI-3DDC84?style=flat&logo=android&logoColor=white)
![Kotlin](https://img.shields.io/badge/Kotlin-7F52FF?style=flat&logo=kotlin&logoColor=white)
![Swift](https://img.shields.io/badge/Swift-F05138?style=flat&logo=swift&logoColor=white)
![CMake](https://img.shields.io/badge/CMake-064F8C?style=flat&logo=cmake&logoColor=white)

**Frameworks & Runtimes**
![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat&logo=nodedotjs&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)
![React Native](https://img.shields.io/badge/React_Native-20232A?style=flat&logo=react&logoColor=61DAFB)
![Qt](https://img.shields.io/badge/Qt-41CD52?style=flat&logo=qt&logoColor=white)

**Cloud & Infrastructure**
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazonwebservices&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=flat&logo=googlecloud&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat&logo=kubernetes&logoColor=white)
![Ansible](https://img.shields.io/badge/Ansible-EE0000?style=flat&logo=ansible&logoColor=white)
![Chef](https://img.shields.io/badge/Chef-F09820?style=flat&logo=chef&logoColor=white)
![Puppet](https://img.shields.io/badge/Puppet-FFAE1A?style=flat&logo=puppet&logoColor=black)

**CI/CD & Build Tools**
![CircleCI](https://img.shields.io/badge/CircleCI-343434?style=flat&logo=circleci&logoColor=white)
![Travis CI](https://img.shields.io/badge/Travis_CI-3EAAAF?style=flat&logo=travisci&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white)
![Gradle](https://img.shields.io/badge/Gradle-02303A?style=flat&logo=gradle&logoColor=white)
![Maven](https://img.shields.io/badge/Maven-C71A36?style=flat&logo=apachemaven&logoColor=white)
![Jira](https://img.shields.io/badge/Jira-0052CC?style=flat&logo=jira&logoColor=white)
![VS Code](https://img.shields.io/badge/VS_Code-007ACC?style=flat&logo=visualstudiocode&logoColor=white)

**Testing**
![Robot Framework](https://img.shields.io/badge/Robot_Framework-000000?style=flat&logo=robotframework&logoColor=white)
![PyTest](https://img.shields.io/badge/PyTest-0A9EDC?style=flat&logo=pytest&logoColor=white)
![Jest](https://img.shields.io/badge/Jest-C21325?style=flat&logo=jest&logoColor=white)
![Mocha](https://img.shields.io/badge/Mocha-8D6748?style=flat&logo=mocha&logoColor=white)
![GoogleTest](https://img.shields.io/badge/GoogleTest-4285F4?style=flat&logo=google&logoColor=white)

**Databases**
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white)
![Elasticsearch](https://img.shields.io/badge/Elasticsearch-005571?style=flat&logo=elasticsearch&logoColor=white)
Relational & NoSQL databases

**Monitoring & Observability**
![Kibana](https://img.shields.io/badge/Kibana-005571?style=flat&logo=kibana&logoColor=white)
![Logstash](https://img.shields.io/badge/Logstash-005571?style=flat&logo=logstash&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat&logo=grafana&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat&logo=prometheus&logoColor=white)
![InfluxDB](https://img.shields.io/badge/InfluxDB-22ADF6?style=flat&logo=influxdb&logoColor=white)

**Platforms**
![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat&logo=windows&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black)
![Android](https://img.shields.io/badge/Android-3DDC84?style=flat&logo=android&logoColor=white)

---

## 🌱 Currently Learning

- 🤖 **Machine Learning** and efficient LLM inference (quantization, MoE, speculative decoding)
- 📱 **Flutter** for cross-platform mobile development
- ⚙️ **Scala**
- 🧩 **Microservices architecture**

---

## 🤝 Let's Collaborate

I'm open to contributing to **open-source projects** and always happy to learn from others. If you're working on something interesting, feel free to reach out!

## 📫 Contact

- **LinkedIn:** [linkedin.com/in/andrei-borcea](https://www.linkedin.com/in/andrei-borcea)
- **Telegram:** [@hustlercoder](https://t.me/hustlercoder)
