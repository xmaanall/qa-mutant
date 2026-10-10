# Architecture

QA-MUTANT has four logical layers:

1. **Demo application** — a fictional ShopSphere business-rule module.
2. **Mutation engine** — creates small, interpretable behavioral changes.
3. **Execution and scoring** — runs pytest and records evidence.
4. **AI-assisted analysis** — interprets surviving mutations and proposes focused test improvements.

The architecture intentionally keeps AI separate from execution truth. The LLM may propose or explain; pytest determines observed behavior.
