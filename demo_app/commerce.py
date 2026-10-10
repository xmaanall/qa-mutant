"""Fictional ShopSphere business rules used by QA-MUTANT."""


def calculate_delivery_fee(subtotal: float) -> float:
    """Free delivery at or above $100; otherwise $10."""
    if subtotal >= 100:
        return 0.0
    return 10.0


def calculate_discount(subtotal: float, coupon: str | None) -> float:
    """VIP10 gives 10% off orders of at least $50, capped at $30."""
    if coupon == "VIP10" and subtotal >= 50:
        return min(subtotal * 0.10, 30.0)
    return 0.0


def calculate_refund(item_price: float, return_days: int, restocking_fee: float = 0.0) -> float:
    """Full refund within 30 days, less a non-negative restocking fee."""
    if return_days < 0:
        raise ValueError("return_days cannot be negative")
    if item_price < 0:
        raise ValueError("item_price cannot be negative")
    if return_days <= 30:
        return max(item_price - max(restocking_fee, 0.0), 0.0)
    return 0.0
