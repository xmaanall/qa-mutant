import json
from pathlib import Path

from engine.runner import run_experiment
from engine.scoring import summarize


if __name__ == "__main__":
    results = run_experiment()
    summary = summarize(results)
    payload = {"summary": summary, "mutations": results}
    out = Path("experiments/baseline_results.json")
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
