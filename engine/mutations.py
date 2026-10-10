"""Small, interpretable mutation operators for the portfolio demo."""

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class Mutation:
    mutation_id: str
    description: str
    source_file: str
    original: str
    replacement: str


TARGET = Path("demo_app/commerce.py")


def generate_mutations() -> list[Mutation]:
    return [
        Mutation("MUT-001", "Delivery boundary: >= becomes >", str(TARGET), "subtotal >= 100", "subtotal > 100"),
        Mutation("MUT-002", "Delivery boundary: >= becomes ==", str(TARGET), "subtotal >= 100", "subtotal == 100"),
        Mutation("MUT-003", "Delivery free branch returns 5 instead of 0", str(TARGET), "if subtotal >= 100:\n        return 0.0", "if subtotal >= 100:\n        return 5.0"),
        Mutation("MUT-004", "Delivery threshold lowered to 90", str(TARGET), "subtotal >= 100", "subtotal >= 90"),
        Mutation("MUT-005", "Discount threshold: >= becomes >", str(TARGET), "subtotal >= 50", "subtotal > 50"),
        Mutation("MUT-006", "Discount percentage changes from 10% to 5%", str(TARGET), "subtotal * 0.10", "subtotal * 0.05"),
        Mutation("MUT-007", "Discount cap increases from 30 to 50", str(TARGET), "30.0", "50.0"),
        Mutation("MUT-008", "Invalid coupons receive a $5 discount", str(TARGET), "if coupon == \"VIP10\" and subtotal >= 50:\n        return min(subtotal * 0.10, 30.0)\n    return 0.0", "if coupon == \"VIP10\" and subtotal >= 50:\n        return min(subtotal * 0.10, 30.0)\n    return 5.0"),
        Mutation("MUT-009", "Refund window: <= becomes <", str(TARGET), "return_days <= 30", "return_days < 30"),
        Mutation("MUT-010", "Refund window extends to 60 days", str(TARGET), "return_days <= 30", "return_days <= 60"),
        Mutation("MUT-011", "Refund subtracts double restocking fee", str(TARGET), "item_price - max(restocking_fee, 0.0)", "item_price - (2 * max(restocking_fee, 0.0))"),
        Mutation("MUT-012", "Refund after window incorrectly returns item price", str(TARGET), "if return_days <= 30:\n        return max(item_price - max(restocking_fee, 0.0), 0.0)\n    return 0.0", "if return_days <= 30:\n        return max(item_price - max(restocking_fee, 0.0), 0.0)\n    return item_price"),
    ]


def apply_mutation(source: str, mutation: Mutation) -> str:
    if mutation.original not in source:
        raise ValueError(f"Mutation target not found: {mutation.original}")
    return source.replace(mutation.original, mutation.replacement, 1)
