import math
import pytest

from cashflows import npv, irr, payback_period, mirr, profitability_index


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


def test_mirr_matches_manual():
    # MIRR with finance=reinvest=10% on [-1000, 200, 300, 400, 500]
    # FV positives = 200*1.1^3 + 300*1.1^2 + 400*1.1 + 500 = 1569.20
    # MIRR = (1569.20/1000)^(1/4) - 1 ~= 0.1192
    flows = [-1000, 200, 300, 400, 500]
    assert mirr(flows, 0.10, 0.10) == pytest.approx(0.1192, abs=1e-3)


def test_mirr_collapses_to_irr_when_rates_match_sign():
    # When finance and reinvest rates equal, MIRR <= IRR for typical cashflows
    flows = [-1000, 500, 500, 500]
    m = mirr(flows, 0.10, 0.10)
    assert 0 < m < irr(flows)


def test_mirr_requires_both_signs():
    with pytest.raises(ValueError):
        mirr([100, 200, 300], 0.1, 0.1)


def test_profitability_index():
    flows = [-1000, 400, 400, 400]
    pi = profitability_index(0.10, flows)
    assert pi == pytest.approx(0.9947, abs=1e-3)


def test_profitability_index_requires_initial_outflow():
    with pytest.raises(ValueError):
        profitability_index(0.1, [100, 100])
