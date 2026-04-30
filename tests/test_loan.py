import pytest
from cashflows import amortize


def test_loan_basic_30y():
    s = amortize(200_000, 0.045, 30)
    # Excel PMT(0.045/12, 360, -200000) ~= 1013.37
    assert s.monthly_payment == pytest.approx(1013.37, abs=0.5)
    assert s.months == 360
    assert s.schedule[-1].balance == pytest.approx(0.0, abs=1e-2)
    assert s.total_interest == pytest.approx(s.total_paid - s.principal)


def test_loan_zero_rate():
    s = amortize(1200, 0.0, 1)
    assert s.monthly_payment == pytest.approx(100.0)
    assert s.total_interest == pytest.approx(0.0, abs=1e-6)
    assert s.schedule[-1].balance == pytest.approx(0.0, abs=1e-6)


def test_loan_invalid_inputs():
    with pytest.raises(ValueError):
        amortize(0, 0.05, 5)
    with pytest.raises(ValueError):
        amortize(1000, 0.05, 0)


def test_loan_principal_recovered():
    s = amortize(50_000, 0.06, 5)
    total_principal = sum(r.principal for r in s.schedule)
    assert total_principal == pytest.approx(50_000, abs=1e-2)
