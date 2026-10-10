from collections import Counter


def summarize(results: list[dict]) -> dict:
    counts = Counter(r["status"] for r in results)
    valid = counts["killed"] + counts["survived"]
    score = (counts["killed"] / valid * 100) if valid else 0.0
    return {
        "total": len(results),
        "killed": counts["killed"],
        "survived": counts["survived"],
        "invalid": counts["invalid"],
        "valid": valid,
        "mutation_score": round(score, 2),
    }
