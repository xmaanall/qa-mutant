"""Run pytest against a temporary mutated copy of the demo application."""

from dataclasses import asdict
from pathlib import Path
import json
import shutil
import subprocess
import tempfile

from .mutations import Mutation, apply_mutation

ROOT = Path(__file__).resolve().parents[1]


def run_baseline() -> dict:
    result = subprocess.run(["python", "-m", "pytest", "-q"], cwd=ROOT, capture_output=True, text=True)
    return {"passed": result.returncode == 0, "returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}


def run_mutation(mutation: Mutation) -> dict:
    source_path = ROOT / mutation.source_file
    original_source = source_path.read_text(encoding="utf-8")
    mutated_source = apply_mutation(original_source, mutation)

    with tempfile.TemporaryDirectory(prefix="qa_mutant_") as tmp:
        tmp_path = Path(tmp)
        shutil.copytree(ROOT / "demo_app", tmp_path / "demo_app")
        shutil.copytree(ROOT / "tests", tmp_path / "tests")
        (tmp_path / "demo_app" / "commerce.py").write_text(mutated_source, encoding="utf-8")
        result = subprocess.run(["python", "-m", "pytest", "-q"], cwd=tmp_path, capture_output=True, text=True)
        return {
            **asdict(mutation),
            "status": "killed" if result.returncode != 0 else "survived",
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }


def run_experiment() -> list[dict]:
    baseline = run_baseline()
    if not baseline["passed"]:
        raise RuntimeError(f"Baseline tests must pass before mutation testing.\n{baseline['stdout']}\n{baseline['stderr']}")
    return [run_mutation(m) for m in __import__("engine.mutations", fromlist=["generate_mutations"]).generate_mutations()]
