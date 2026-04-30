from typing import Sequence
from .core import npv, irr, payback_period, profitability_index, mirr
from . import ui, charts


def render_analysis(rate: float, cashflows: Sequence[float]) -> str:
    out = []
    out.append(ui.header("ANALISIS DE FLUJO DE CAJA"))
    out.append("")

    labels = [f"t={i}" for i in range(len(cashflows))]
    out.append(ui.bold(ui.cyan("Flujos en el tiempo")))
    out.append(charts.horizontal_bars(cashflows, labels=labels, width=40))
    out.append("")

    invested = -sum(cf for cf in cashflows if cf < 0)
    received = sum(cf for cf in cashflows if cf > 0)
    net = sum(cashflows)

    summary = [
        f"{ui.bold('Total invertido:'):<22} {ui.colored_money(-invested, 14)}",
        f"{ui.bold('Total recuperado:'):<22} {ui.colored_money(received, 14)}",
        f"{ui.bold('Ganancia bruta:'):<22} {ui.colored_money(net, 14)}",
    ]
    out.append(ui.box("CAJA", summary, width=50, color=ui.gray))
    out.append("")

    npv_val = npv(rate, cashflows)
    try:
        irr_val = irr(cashflows)
        irr_str = ui.colored_pct(irr_val, 14)
    except Exception:
        irr_val = None
        irr_str = ui.gray("           n/a")

    try:
        mirr_val = mirr(cashflows, rate, rate)
        mirr_str = ui.colored_pct(mirr_val, 14)
    except Exception:
        mirr_val = None
        mirr_str = ui.gray("           n/a")

    pb = payback_period(cashflows)
    pb_str = ui.cyan(f"{pb:>11.2f} per") if pb is not None else ui.red("        nunca")

    try:
        pi = profitability_index(rate, cashflows)
        pi_str = (ui.green if pi >= 1 else ui.red)(f"{pi:>14.3f}")
    except Exception:
        pi = None
        pi_str = ui.gray("           n/a")

    metrics = [
        f"{ui.bold('Tasa descuento:'):<22} {ui.cyan(f'{rate*100:>13.2f}%')}",
        f"{ui.bold('NPV:'):<22} {ui.colored_money(npv_val, 14)}",
        f"{ui.bold('IRR:'):<22} {irr_str}",
        f"{ui.bold('MIRR:'):<22} {mirr_str}",
        f"{ui.bold('Payback:'):<22} {pb_str}",
        f"{ui.bold('Profitability Idx:'):<22} {pi_str}",
    ]
    out.append(ui.box("METRICAS", metrics, width=50, color=ui.cyan))
    out.append("")

    verdict_lines = []
    if npv_val > 0:
        verdict_lines.append(ui.green("[OK] NPV positivo: la inversion crea valor."))
    else:
        verdict_lines.append(ui.red("[X]  NPV negativo: la inversion destruye valor."))

    if irr_val is not None:
        if irr_val > rate:
            verdict_lines.append(ui.green(f"[OK] IRR ({irr_val*100:.2f}%) > tasa exigida ({rate*100:.2f}%)."))
        else:
            verdict_lines.append(ui.red(f"[X]  IRR ({irr_val*100:.2f}%) <= tasa exigida ({rate*100:.2f}%)."))

    if pi is not None:
        if pi >= 1:
            verdict_lines.append(ui.green(f"[OK] Indice de rentabilidad {pi:.3f} >= 1."))
        else:
            verdict_lines.append(ui.red(f"[X]  Indice de rentabilidad {pi:.3f} < 1."))

    decision = "INVERTIR" if (npv_val > 0 and (irr_val is None or irr_val > rate)) else "RECHAZAR"
    color = ui.green if decision == "INVERTIR" else ui.red
    verdict_lines.append("")
    verdict_lines.append(ui.bold(color(f">>> RECOMENDACION: {decision} <<<")))
    out.append(ui.box("VEREDICTO", verdict_lines, width=58, color=ui.yellow))
    return "\n".join(out)


def render_sensitivity(cashflows: Sequence[float], rates: Sequence[float]) -> str:
    points = [(r, npv(r, cashflows)) for r in rates]
    out = [ui.header("ANALISIS DE SENSIBILIDAD - NPV vs TASA")]
    out.append("")
    out.append(charts.line_chart(points, width=50, height=12, title="NPV(rate)"))
    out.append("")
    out.append(ui.gray(f" {'Tasa':>8} | {'NPV':>14}"))
    out.append(ui.gray(" " + "-" * 26))
    for r, v in points:
        out.append(f" {r*100:>7.2f}% | {ui.colored_money(v, 14)}")
    try:
        irr_val = irr(cashflows)
        out.append("")
        out.append(ui.bold(ui.cyan(f"IRR (cruce con NPV=0): {irr_val*100:.4f}%")))
    except Exception:
        pass
    return "\n".join(out)
