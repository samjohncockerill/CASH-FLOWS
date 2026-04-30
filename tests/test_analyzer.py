from cashflows.analyzer import render_analysis, render_sensitivity
from cashflows.charts import horizontal_bars, line_chart
from cashflows.loan import amortize, render_loan_report
from cashflows import ui


def setup_module(_):
    ui.set_color(False)


def test_render_analysis_runs():
    out = render_analysis(0.10, [-1000, 400, 400, 400])
    assert "ANALISIS" in out
    assert "NPV" in out
    assert "IRR" in out
    assert "RECOMENDACION" in out


def test_render_sensitivity_runs():
    out = render_sensitivity([-1000, 400, 400, 400], [0.0, 0.05, 0.10, 0.15, 0.20])
    assert "SENSIBILIDAD" in out


def test_horizontal_bars_runs():
    out = horizontal_bars([-100, 50, 50, 50])
    assert isinstance(out, str) and len(out) > 0


def test_line_chart_runs():
    pts = [(0.0, 100.0), (0.1, 50.0), (0.2, 0.0), (0.3, -25.0)]
    out = line_chart(pts, width=20, height=6)
    assert isinstance(out, str) and len(out) > 0


def test_render_loan_report_runs():
    s = amortize(10_000, 0.05, 1)
    out = render_loan_report(s)
    assert "AMORTIZACION" in out
    assert "Cuota" in out
