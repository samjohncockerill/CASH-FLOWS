from typing import Sequence, Optional


def npv(rate: float, cashflows: Sequence[float]) -> float:
    if rate <= -1:
        raise ValueError("rate must be greater than -1")
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(cashflows))


def irr(
    cashflows: Sequence[float],
    guess: float = 0.1,
    tol: float = 1e-7,
    max_iter: int = 200,
) -> float:
    if not cashflows or all(cf >= 0 for cf in cashflows) or all(cf <= 0 for cf in cashflows):
        raise ValueError("cashflows must contain at least one positive and one negative value")

    rate = guess
    for _ in range(max_iter):
        f = sum(cf / (1 + rate) ** t for t, cf in enumerate(cashflows))
        df = sum(-t * cf / (1 + rate) ** (t + 1) for t, cf in enumerate(cashflows))
        if df == 0:
            break
        new_rate = rate - f / df
        if abs(new_rate - rate) < tol:
            return new_rate
        rate = new_rate
    raise RuntimeError("IRR did not converge")


def payback_period(cashflows: Sequence[float]) -> Optional[float]:
    cumulative = 0.0
    for t, cf in enumerate(cashflows):
        prev = cumulative
        cumulative += cf
        if cumulative >= 0 and prev < 0:
            needed = -prev
            if cf == 0:
                return float(t)
            return (t - 1) + needed / cf
    return None
