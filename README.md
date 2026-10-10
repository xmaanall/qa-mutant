# QA-MUTANT 🧬

**An AI-powered adversarial testing framework for measuring and improving test-suite strength.**

QA-MUTANT flips the usual AI-testing idea. Instead of asking AI to simply generate more test cases, it creates targeted mutations of application behavior, runs an existing test suite against those mutations, identifies surviving mutations, and uses AI-assisted analysis to propose targeted tests.

> **The goal is not to generate more tests. The goal is to build stronger tests that can detect more defects.**

## What it does

1. Runs a baseline pytest suite against a small fictional e-commerce application.
2. Creates controlled mutations of business logic.
3. Executes the test suite against each mutant.
4. Classifies mutants as **killed**, **survived**, or **invalid**.
5. Calculates a mutation score.
6. Analyzes surviving mutants and suggests targeted tests.
7. Provides a Streamlit dashboard for the experiment.

## Demo domain

The project uses a fictional e-commerce application called **ShopSphere**. It has no connection to any real company, production system, government platform, or private data.

## Project structure

```text
qa-mutant/
├── app/                    # Streamlit dashboard
├── engine/                 # Mutation and scoring engine
├── ai/                     # AI-assisted analysis layer
├── demo_app/               # Fictional application under test
├── tests/                  # Baseline test suite
├── experiments/            # Reproducible experiment outputs
├── docs/                   # Architecture and methodology
├── .github/workflows/      # CI
├── requirements.txt
└── README.md
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q
python -m engine.run_experiment
streamlit run app/dashboard.py
```

The live LLM analysis is optional. Without an API key, QA-MUTANT uses a deterministic local analysis fallback so the core experiment remains reproducible. To enable live OpenAI analysis, set `OPENAI_API_KEY` and optionally `OPENAI_MODEL` in your environment. API usage may incur charges. The current mutation operators are deterministic; the LLM analyzes surviving mutations and proposes focused tests.

To enable an LLM provider, copy `.env.example` to `.env` and configure the provider supported by your environment.

## Metrics

**Mutation Score**

```text
Killed valid mutants / Total valid mutants × 100
```

The dashboard also reports surviving mutants and AI recommendations. AI suggestions are treated as proposals and are never considered valid merely because the model generated them.

## Important methodology

QA-MUTANT separates **execution evidence** from **AI interpretation**. The test runner determines whether a mutant was killed or survived. AI can explain a gap or propose a test, but it cannot override execution results.

For a rigorous experiment, future versions should evaluate AI-generated tests on a hold-out mutant set that was not used during generation.

## Limitations

- This is an experimental portfolio project, not a production mutation-testing platform.
- The initial mutation operators are intentionally small and interpretable.
- Some surviving mutants can be behaviorally equivalent to the original implementation and require review.
- LLM output can be incorrect; recommendations require validation.

## Roadmap

- [x] Deterministic mutation engine
- [x] Mutation execution and scoring
- [x] Surviving-mutant analysis
- [x] Streamlit dashboard
- [x] CI workflow
- [ ] Hold-out evaluation for AI-generated tests
- [ ] More language-aware mutation operators
- [ ] Historical experiment comparison
- [ ] Automated test patch validation

## License

MIT
