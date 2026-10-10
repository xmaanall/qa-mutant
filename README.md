# QA-MUTANT --- AI-Powered Adversarial Testing Framework

An AI-assisted mutation testing framework designed to identify test
coverage gaps, analyze surviving mutations, and guide the creation of
stronger software tests.

## Project Goal

QA-MUTANT simulates adversarial changes to application logic and
measures whether the existing test suite can detect them.

The framework analyzes surviving mutations and generates focused testing
recommendations to improve test coverage.

## How It Works

``` text
Application Code
       ↓
Mutation Engine
       ↓
Generate Mutants
       ↓
Run Test Suite
       ↓
Killed / Survived
       ↓
AI Analysis
       ↓
Testing Recommendations
       ↓
Add Stronger Tests
       ↓
Re-run Mutation Testing
```

## Project Structure

``` text
qa-mutant/
├── demo_app/
│   └── commerce.py
├── tests/
│   └── test_commerce.py
├── engine/
│   ├── mutations.py
│   ├── runner.py
│   ├── scoring.py
│   └── run_experiment.py
├── ai/
│   └── analyzer.py
├── experiments/
│   ├── baseline_results.json
│   ├── improved_results.json
│   └── ai_analysis.json
└── README.md
```

## Mutation Testing

The project introduces controlled changes to application logic,
including boundary conditions, thresholds, branch behavior, discount
rules, and other business rules.

-   **Killed** → at least one test detects the changed behavior.
-   **Survived** → the current test suite does not detect the changed
    behavior.

## Results

### Baseline

  Metric                  Result
  ----------------- ------------
  Total Mutations             12
  Killed                       8
  Survived                     4
  Mutation Score      **66.67%**

### AI Analysis

The AI analysis layer reviews surviving mutations and generates focused
testing recommendations, such as boundary tests, exact monetary
assertions, and focused branch assertions.

The analyzer supports a deterministic local fallback and optional OpenAI
Responses API integration.

### Improved Test Suite

After adding targeted tests based on the identified gaps:

  Metric                Result
  ----------------- ----------
  Total Mutations           12
  Killed                    12
  Survived                   0
  Mutation Score      **100%**

## Running the Project

``` bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python -m engine.run_experiment
```

Run AI analysis against the baseline:

``` bash
python -c 'import json; from ai.analyzer import analyze_results; data=json.load(open("experiments/baseline_results.json")); findings=analyze_results(data["mutations"], use_llm=False); json.dump(findings, open("experiments/ai_analysis.json","w"), indent=2); print(json.dumps(findings, indent=2))'
```

## Why Mutation Testing?

Traditional code coverage can show that a line was executed without
proving that the test actually validates the expected behavior.

Mutation testing introduces intentional faults and checks whether the
tests detect them.

## Key Outcome

**66.67% → 100% mutation score**

**4 → 0 surviving mutations**

QA-MUTANT demonstrates an adversarial QA workflow:

**Introduce defects → Detect weak tests → Analyze gaps → Strengthen
tests → Re-measure quality**

## Technologies

-   Python
-   pytest
-   Mutation Testing
-   JSON
-   Git / GitHub
-   OpenAI Responses API
-   AI-assisted testing

## Author

**Manal Alotaibi**

QA / Software Testing

Focus areas: Quality Assurance, Software Testing, API Testing, Test
Automation, AI-Assisted Testing, Adversarial Testing.
