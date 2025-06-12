# 🏆 Hackathon Project: Dependency Agent

**By:** Abdul Hakim Norazman & James Thompson  
**Team:** AM Research Tech

---

## 🧩 The Problem

Modern coding assistants like GitHub Copilot excel at boilerplate suggestions but fall short when it comes to **resolving complex dependency issues**. Why?

- Lack of context from dependency changelogs results in infinite upgrade/downgrade loops.
- OpenRewrite recipes can make breaking changes that require manual review.
- Upgrading frameworks or remediating FARM vulnerabilities steals time from business-critical features.

---

## 🧪 Example Scenarios

- Jackson version bumps cause transitive dependency mismatches.
- Logback and Log4j conflict silently at runtime.
- Framework upgrades break multi-module Maven builds unexpectedly.

---

## 💡 Our Solution

We built a smart **Dependency Agent** that automates this workflow:

1. Detects Maven compile or build failures.
2. Uses OpenAI to search Google for changelog information (e.g. "jackson 2.9.8 to 2.14.0").
3. Understands the context and recommends or applies changes to fix the error.

---

## 👥 Who Benefits?

- Teams working on Moneta upgrades
- FARM break owners
- Engineering teams looking to reduce BAU overhead

---

## 🛠️ Tech Stack

- **Java + Maven**: Project simulation and builds.
- **Python + `uv` + `just`**: Tooling and automation layer.
- **OpenAI API**: Changelog-aware resolution logic.

---

## 📦 Scalability & Prod Readiness

- Language-agnostic design for broader dependency manager support.
- Integration planned with internal **LLMSuite API**.
- Token efficiency optimized via JSON formatting and screen scraping fallback.
- Explorer diffing between changelog jars.

---

## ⚠️ Known Limitations

- Large changelogs may hit token limits.
- Relies on Google search quality for changelog availability.
- Broader test coverage across Maven patterns still needed.
- Not all changees are documented fully.

---

## ❓ Judge Q&A

- **Can it support other packages?** Yes, designed with pluggable dependency resolvers.
- **How are multiple changelogs handled?** Through context-aware parsing and heuristics.
- **Why not LLM Suite?** Access wasn’t available during the hackathon window.

---

## 📂 See Also

- [README.md](../README.md)
- [`mvn1`, `log4j_broken_build`, etc. in `justfile`](../justfile)
- Sample conflict projects under `/maven/`
