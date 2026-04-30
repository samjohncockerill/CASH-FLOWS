import math
import pytest

from cashflows import npv, irr, payback_period


def test_npv_zero_rate_is_sum():
    flows = [-100, 50, 60, 70]
    assert npv(0.0, flows) == pytest.approx(80.0)


def test_npv_positive_rate():
    flows = [-1000, 400, 400, 400]
    assert npv(0.1, flows) == pytest.approx(-5.2592, rel=1e-3)


def test_npv_invalid_rate():
    with pytest.raises(ValueError):
        npv(-1.0, [-100, 50, 60])


def test_irr_basic():
    flows = [-1000, 500, 500, 500]
    rate = irr(flows)
    assert rate == pytest.approx(0.2337, rel=1e-3)
    assert math.isclose(npv(rate, flows), 0.0, abs_tol=1e-6)


def test_irr_requires_sign_change():
    with pytest.raises(ValueError):
        irr([100, 200, 300])


def test_payback_period_simple():
    flows = [-1000, 400, 400, 400]
    assert payback_period(flows) == pytest.approx(2.5)


def test_payback_period_never():
    assert payback_period([-100, 10, 10]) is None
