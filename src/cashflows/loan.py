from dataclasses import dataclass
from typing import List
from . import ui


@dataclass
class AmortizationRow:
    period: int
    payment: float
    interest: float
    principal: float
    balance: float


@dataclass
class LoanSummary:
    principal: float
    annual_rate: float
    months: int
    monthly_payment: float
    total_paid: float
    total_interest: float
    schedule: List[AmortizationRow]


def amortize(principal: float, annual_rate: float, years: float) -> LoanSummary:
    if principal <= 0:
        raise ValueError("principal must be positive")
    if years <= 0:
        raise ValueError("years must be positive")
    months = int(round(years * 12))
    r = annual_rate / 12.0
    if r == 0:
        payment = principal / months
    else:
        payment = principal * (r * (1 + r) ** months) / ((1 + r) ** months - 1)

    schedule: List[AmortizationRow] = []
    balance = principal
    for m in range(1, months + 1):
        interest = balance * r
        prin = payment - interest
        balance = max(0.0, balance - prin)
        schedule.append(AmortizationRow(m, payment, interest, prin, balance))

    total_paid = payment * months
    return LoanSummary(
        principal=principal,
        annual_rate=annual_rate,
        months=months,
        monthly_payment=payment,
        total_paid=total_paid,
        total_interest=total_paid - principal,
        schedule=schedule,
    )


def render_loan_report(summary: LoanSummary, max_rows: int = 12) -> str:
    s = summary
    lines = []
    lines.append(ui.header("AMORTIZACION DE PRESTAMO"))
    lines.append("")

    box_lines = [
        f"{ui.bold('Capital:'):<18} {ui.colored_money(s.principal, 14)}",
        f"{ui.bold('Tasa anual:'):<18} {ui.cyan(f'{s.annual_rate*100:>13.2f}%')}",
        f"{ui.bold('Plazo:'):<18} {ui.cyan(f'{s.months:>10} meses')}",
        f"{ui.bold('Cuota mensual:'):<18} {ui.colored_money(s.monthly_payment, 14)}",
        f"{ui.bold('Total a pagar:'):<18} {ui.colored_money(s.total_paid, 14)}",
        f"{ui.bold('Total intereses:'):<18} {ui.colored_money(s.total_interest, 14)}",
        f"{ui.bold('% sobrecoste:'):<18} {ui.yellow(f'{s.total_interest/s.principal*100:>13.2f}%')}",
    ]
    lines.append(ui.box("RESUMEN", box_lines, width=58, color=ui.cyan))
    lines.append("")

    lines.append(ui.bold(ui.cyan("DETALLE DE AMORTIZACION (primeros y ultimos meses)")))
    header_row = (
        f" {'Mes':>4} | {'Cuota':>12} | {'Interes':>12} | {'Capital':>12} | {'Saldo':>14}"
    )
    lines.append(ui.gray(header_row))
    lines.append(ui.gray(" " + "-" * (len(header_row) - 1)))

    rows = s.schedule
    show = list(range(min(max_rows // 2, len(rows))))
    if len(rows) > max_rows:
        gap_marker = True
        show += list(range(len(rows) - max_rows // 2, len(rows)))
    else:
        gap_marker = False
        show = list(range(len(rows)))

    last_idx = -2
    for i in show:
        if gap_marker and i - last_idx > 1:
            lines.append(ui.gray(f" {'...':>4} | {'...':>12} | {'...':>12} | {'...':>12} | {'...':>14}"))
        row = rows[i]
        lines.append(
            f" {row.period:>4} | "
            f"{ui.colored_money(row.payment, 12)} | "
            f"{ui.red(f'{row.interest:>12,.2f}')} | "
            f"{ui.green(f'{row.principal:>12,.2f}')} | "
            f"{ui.cyan(f'{row.balance:>14,.2f}')}"
        )
        last_idx = i

    return "\n".join(lines)
