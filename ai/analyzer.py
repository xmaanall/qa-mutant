"""AI-assisted analysis with optional OpenAI Responses API integration.

Without OPENAI_API_KEY, the project uses a deterministic local fallback so the
experiment remains runnable and reproducible at zero API cost.
"""

import json
import os


def _fallback(mutation: dict) -> dict:
    description = mutation["description"]
    lower = description.lower()
    mapping = {
        "boundary": "Add values immediately below, exactly at, and immediately above the business threshold.",
        "threshold": "Add values immediately below, exactly at, and immediately above the business threshold.",
        "percentage": "Verify the expected percentage with representative values and assert the exact monetary result.",
        "cap": "Add a case that exceeds the cap and assert the exact capped value.",
        "window": "Add tests immediately before, exactly at, and immediately after the allowed time window.",
        "fee": "Verify the calculation with a non-zero fee and assert the exact expected amount.",
        "coupon": "Add a test for an invalid coupon and assert that the discount is exactly zero.",
        "discount": "Add invalid-coupon and boundary scenarios and assert exact monetary outcomes.",
        "price": "Verify the behavior when the rule is no longer satisfied and assert the exact returned amount.",
    }
    recommendation = next((v for k, v in mapping.items() if k in lower),
                          "Review the changed behavior and add a focused assertion that distinguishes the original from the mutation.")
    return {
        "mutation_id": mutation["mutation_id"],
        "finding": "Potential test coverage gap",
        "confidence": "medium",
        "recommendation": recommendation,
        "evidence": description,
        "provider": "deterministic-fallback",
    }


def analyze_results(results: list[dict], use_llm: bool = False) -> list[dict]:
    survivors = [r for r in results if r["status"] == "survived"]
    if not survivors:
        return []

    api_key = os.getenv("OPENAI_API_KEY")
    if use_llm and api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            compact = [{"mutation_id": r["mutation_id"], "description": r["description"],
                        "changed_code": f"{r['original']} -> {r['replacement']}"} for r in survivors]
            response = client.responses.create(
                model=os.getenv("OPENAI_MODEL", "gpt-6-luna"),
                instructions=(
                    "You are a senior software test engineer. Analyze surviving mutations and propose "
                    "focused tests. Treat each finding as a hypothesis, not a confirmed defect. "
                    "Return only valid JSON: an array of objects with mutation_id, finding, confidence, "
                    "recommendation, and evidence. Do not claim tests were executed."
                ),
                input=json.dumps(compact),
            )
            parsed = json.loads(response.output_text)
            if isinstance(parsed, list):
                return [{**item, "provider": "openai-responses-api"} for item in parsed]
        except Exception as exc:
            fallback = [_fallback(r) for r in survivors]
            for item in fallback:
                item["provider"] = f"fallback (LLM unavailable: {type(exc).__name__})"
            return fallback

    return [_fallback(r) for r in survivors]
