from demo_app.commerce import calculate_delivery_fee, calculate_discount, calculate_refund


def test_delivery_below_threshold():
    assert calculate_delivery_fee(99.99) == 10.0


def test_vip_discount_below_threshold():
    assert calculate_discount(49.99, "VIP10") == 0.0


def test_vip_discount_is_capped():
    assert calculate_discount(500, "VIP10") == 30.0


def test_invalid_coupon_gets_no_discount():
    assert calculate_discount(100, "NOPE") == 0.0


def test_refund_within_window():
    assert calculate_refund(100, 30) == 100.0


def test_refund_after_window():
    assert calculate_refund(100, 31) == 0.0


def test_refund_restocking_fee():
    assert calculate_refund(100, 10, 15) == 85.0


def test_negative_days_are_rejected():
    try:
        calculate_refund(100, -1)
        assert False
    except ValueError:
        pass


def test_delivery_at_free_shipping_boundary():
    assert calculate_delivery_fee(100) == 0.0


def test_delivery_above_free_shipping_boundary():
    assert calculate_delivery_fee(100.01) == 0.0


def test_vip_discount_at_threshold():
    assert calculate_discount(50, "VIP10") == 5.0
