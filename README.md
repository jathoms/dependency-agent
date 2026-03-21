# Dependency Agent - 2025 Hackathon

This project contains multi-module Maven configurations designed to demonstrate how generative AI can be used to solve version conflicts in Java-based systems.

In particular, this repository includes:

* A **working Maven multi-module setup** with Jackson dependencies managed via `dependencyManagement`.
* A **broken version** of the same setup, intentionally introducing a Jackson version mismatch to simulate dependency resolution conflicts.
* A Python support layer using `uv` to sandbox and script auxiliary tasks.
* A `justfile` to simplify common operations.

This project was developed during an internal hackathon by Abdul Hakim Norazman and James Thomson from JPMC.

**Goal:** Create a smart assistant that helps resolve Maven dependency conflicts by analyzing errors, fetching changelogs, and suggesting code fixes.

**Tech Stack:**
- Java + Maven
- Python with `uv` and `just`
- OpenAI API for changelog-aware suggestions

**Key Use Cases:**
- Fixing Jackson version mismatches
- Resolving SLF4J binding issues
- FARM vulnerability remediations

👉 Full write-up available in [`docs/HACKATHON.md`](docs/HACKATHON.md)


---
## 🐍 Get Python 3.13

Install Python 3.13 however you'd like (e.g., from [python.org](https://www.python.org/downloads/) or using `pyenv`).

---

## ⚡ Get `uv`

Install `uv` using `pip`:

```bash
pip install uv
```

---

## 📆 Create a virtual environment

Create and activate a `uv`-managed virtual environment:

```bash
uv venv
```

---

## 💪 Build and Run with `uv`

* To build the project wheel:

  ```bash
  uv build
  ```

* To run a command inside the venv:

  ```bash
  uv run <your-command>
  ```

---

## 💡 Learn More About `uv`

To explore what `uv` can do:

```bash
uv help
```

---

## 🧾 Get `just` (Optional, but Recommended)

[`just`](https://github.com/casey/just) is a handy command runner for developer scripts.

### Install:

1. Install the Rust toolchain from [rustup.rs](https://rustup.rs/)
2. Then install `just`:

   ```bash
   cargo install just
   ```

---

## ⚙️ Use `just`

Run helpful project commands using `just`:

| Command           | Description                                         |
| ----------------- | --------------------------------------------------- |
| `just go`         | Run the Python entry point using `uv`               |
| `just mvn1`       | Build the working Maven setup (requires JDK 21)     |
| `just mvnbroken1` | Build the broken Maven setup (intentional conflict) |

---

## 🧪 Notes

* Maven builds rely on a working Java 21+ environment.
* The broken Maven project demonstrates dependency resolution failure when a child module overrides a managed version.
* `uv` and `just` streamline the Python-side of tooling while keeping Java project logic intact.

---
