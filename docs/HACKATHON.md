# 🏆 Hackathon Project: Dependency Agent

**By:** Abdul Hakim Norazman & James Thompson
**Team:** AM Research Tech

---

## 🧩 The Problem

Modern coding assistants like GitHub Copilot excel at boilerplate suggestions but fall short when it comes to **resolving complex dependency issues**. Why?

* Lack of context from dependency changelogs results in infinite upgrade/downgrade loops.
* OpenRewrite recipes can make breaking changes that require manual review.
* Upgrading frameworks or remediating FARM vulnerabilities steals time from business-critical features.

---

## 🧪 Example Scenarios

* Jackson version bumps cause transitive dependency mismatches.
* Logback and Log4j conflict silently at runtime.
* Framework upgrades break multi-module Maven builds unexpectedly.

---

## 💡 Our Solution

We built a smart **Dependency Agent** that automates this workflow:

1. Detects Maven compile or build failures.
2. Uses OpenAI to search Google for changelog information (e.g. "jackson 2.9.8 to 2.14.0").
3. Understands the context and recommends or applies changes to fix the error.

---

## 👥 Who Benefits?

* Teams working on Moneta upgrades
* FARM break owners
* Engineering teams looking to reduce BAU overhead

---

## 🛠️ Tech Stack

* **Java + Maven**: Project simulation and builds.
* **Python + `uv` + `just`**: Tooling and automation layer.
* **OpenAI API**: Changelog-aware resolution logic.

---

## 📦 Scalability & Prod Readiness

* Language-agnostic design for broader dependency manager support.
* Integration planned with internal **LLMSuite API**.
* Token efficiency optimized via JSON formatting and screen scraping fallback.
* Explorer diffing between changelog jars.

---

## ⚠️ Known Limitations

* Large changelogs may hit token limits.
* Relies on Google search quality for changelog availability.
* Broader test coverage across Maven patterns still needed.
* Not all changees are documented fully.

---

## ❓ Judge Q\&A

**1. What specific pain‑points did you observe in your own workflow that motivated this hackathon project?**
We frequently switch from Windows to Linux environments without seamless tool access, lack internal LLMSuite integration, and encounter AI hallucinations when simulating complex dependency test-cases.

**2. How does the Dependency Agent improve upon existing tools like Dependabot, Renovate, or manual changelog inspection?**
Unlike generic version bump tools, our agent uses real‑time context from changelogs—scraped and parsed by LLM—to recommend precise fixes, avoiding endless upgrade loops and reducing manual diff reviews that Dependabot or Renovate often leave unresolved.

**3. Can you quantify (even roughly) how much time or effort your prototype saves teams during a typical framework upgrade?**
On average, it can save **2–4 hours** per complex dependency break by pinpointing the exact change needed instead of manual root‑cause analysis.

**4. Walk us through the end-to-end flow: from a Maven build error to a resolved dependency change.**
The agent captures the Maven error, sends it to the LLM, screen‑scrapes relevant changelog entries online, interprets breaking vs. minor fixes, and outputs a tailored `pom.xml` diff or CLI patch suggestion.

**5. How do you scrape or retrieve changelog content from Google search results without hitting legal or technical barriers?**
We abide by `robots.txt` policies, cache responses to minimize repeated requests, and limit frequency per domain—while falling back to direct GitHub Releases APIs where available.

**6. What heuristics or ML techniques does your LLM-based resolver use to distinguish breaking vs. non-breaking changes in a changelog?**
We apply semantic similarity scoring on changelog entries against the error context, prioritize sections containing keywords like "BREAKING", "Deprecated", or version ranges, and use embedding‑based classification to flag high‑risk changes.

**7. You mention a language‑agnostic design—what would it take to add support for npm, pip, or Gradle?**
Simply swap the CLI command for dependency trees (e.g., `npm ls`, `pipdeptree`, `gradle dependencies`) and adjust the argument parser—our resolver logic remains identical.

**8. How would you integrate the Dependency Agent into an existing CI/CD pipeline (e.g., Jenkins, GitHub Actions)?**
We’d package the agent as a CLI tool or Docker container, then call it as a pre-build step in Jenkins pipelines or a GitHub Action—automatically opening a PR with suggested fixes when errors occur.

**9. What safeguards (tests, rollbacks) are in place to ensure an automated dependency change doesn’t break production?**
Each suggested change is validated against a sandboxed test suite; fixes are proposed as pull requests requiring developer approval, and we maintain rollback scripts to revert changes if downstream tests fail.

**10. Changelogs can get very large—how do you handle token limits and performance in your OpenAI calls?**
We first identify relevant version ranges within a tolerance window, then screen‑scrape only those sections of the changelog, reducing token usage while capturing the most critical entries.

**11. How do you manage versioning and caching of parsed changelog data to avoid repeated Google searches?**
Parsed changelog entries are stored in a local cache indexed by artifact and version; cache entries expire after configurable TTL (e.g., one week), minimizing redundant searches.

**12. What monitoring or alerting would you build around the agent in a real-world environment?**
We’d integrate with Prometheus/Grafana to track metrics like search latency, fix success rates, and PR merge times, and configure Slack or email alerts for repeated failures or high-risk changes.

**13. Does your solution expose any security risk by downloading or executing untrusted changelog content?**
We treat changelogs as plain text, sanitize all HTML or scripts before parsing, and never execute arbitrary code from external sources—ensuring only text content is processed.

**14. How do you ensure that no malicious code or undesirable side-effects slip through when automatically applying patches?**
Automated suggestions are minimal diffs applied to dependency declarations only; we cross-check with internal vulnerability scanners and require manual code review before merging.

**15. What does the developer interface look like—CLI prompts, dashboards, IDE plug-in?**
Developers interact via `just update-deps` or `python agent.py fix`, which prints suggested diffs in the terminal or opens a local web dashboard for review.

**16. How much manual review do you expect users to perform after the agent proposes a fix?**
Users should review the proposed change summary—filtering out any hallucinations or irrelevant recommendations—before merging.

**17. Can users provide feedback or “teach” the agent when it recommends an incorrect change?**
Yes—by re-running with custom prompt overrides or providing example patches; future versions will include explicit feedback loops to refine the LLM prompt automatically.

**18. Could you demo a live scenario where a Log4j conflict is detected and resolved end-to-end?**
Yes—a sample project under `/maven/log4j_broken_build` demonstrates the full detection-and-fix workflow.

**19. What key metrics (e.g. build-fix time, number of manual interventions) will you track to measure success?**
We’ll track build-to-fix latency, number of LLM calls per fix, token consumption, and reduction in manual interventions during pilot programs on Moneta Spring upgrades.

**20. Have you benchmarked performance across different project sizes or dependency graphs?**
Initial benchmarks record average run-times and token usage across small (<50 deps), medium (50–200 deps), and large (>200 deps) projects—details available in our internal metrics dashboard.

---

## 📂 See Also

- [README.md](../README.md)
- [`mvn1`, `log4j_broken_build`, etc. in `justfile`](../justfile)
- Sample conflict projects under `/maven/`