import argparse
from .core import npv, irr, payback_period
from .analyzer import render_analysis, render_sensitivity
from .loan import amortize, render_loan_report
from . import ui


def _parse_flows(values):
    return [float(v) for v in values]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="cashflows", description="Analizador de flujos de caja e inversiones."
    )
    parser.add_argument("--no-color", action="store_true", help="Desactiva colores ANSI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_npv = sub.add_parser("npv", help="Valor Presente Neto")
    p_npv.add_argument("--rate", type=float, required=True)
    p_npv.add_argument("flows", nargs="+")

    p_irr = sub.add_parser("irr", help="Tasa Interna de Retorno")
    p_irr.add_argument("flows", nargs="+")

    p_pb = sub.add_parser("payback", help="Periodo de recuperacion")
    p_pb.add_argument("flows", nargs="+")

    p_an = sub.add_parser("analyze", help="Analisis completo con grafico y veredicto")
    p_an.add_argument("--rate", type=float, required=True, help="Tasa de descuento (ej. 0.10)")
    p_an.add_argument("flows", nargs="+")

    p_sens = sub.add_parser("sensitivity", help="NPV vs tasa de descuento (grafico)")
    p_sens.add_argument("--from", dest="r_from", type=float, default=0.0)
    p_sens.add_argument("--to", dest="r_to", type=float, default=0.30)
    p_sens.add_argument("--step", type=float, default=0.02)
    p_sens.add_argument("flows", nargs="+")

    p_loan = sub.add_parser("loan", help="Cuadro de amortizacion de prestamo")
    p_loan.add_argument("--principal", type=float, required=True)
    p_loan.add_argument("--rate", type=float, required=True, help="Tasa anual (ej. 0.045)")
    p_loan.add_argument("--years", type=float, required=True)
    p_loan.add_argument("--rows", type=int, default=12, help="Filas del cuadro a mostrar")

    p_serve = sub.add_parser("serve", help="Lanza la app web local")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=8000)
    p_serve.add_argument("--open", action="store_true", help="Abre el navegador automaticamente")

    args = parser.parse_args(argv)
    if args.no_color:
        ui.set_color(False)

    if args.cmd == "npv":
        flows = _parse_flows(args.flows)
        print(f"{npv(args.rate, flows):.6f}")
    elif args.cmd == "irr":
        flows = _parse_flows(args.flows)
        print(f"{irr(flows):.6f}")
    elif args.cmd == "payback":
        flows = _parse_flows(args.flows)
        result = payback_period(flows)
        print("never" if result is None else f"{result:.6f}")
    elif args.cmd == "analyze":
        flows = _parse_flows(args.flows)
        print(render_analysis(args.rate, flows))
    elif args.cmd == "sensitivity":
        flows = _parse_flows(args.flows)
        rates = []
        r = args.r_from
        while r <= args.r_to + 1e-9:
            rates.append(round(r, 6))
            r += args.step
        print(render_sensitivity(flows, rates))
    elif args.cmd == "loan":
        summary = amortize(args.principal, args.rate, args.years)
        print(render_loan_report(summary, max_rows=args.rows))
    elif args.cmd == "serve":
        from .web import serve_forever
        if args.open:
            import webbrowser, threading
            threading.Timer(0.5, lambda: webbrowser.open(f"http://{args.host}:{args.port}/")).start()
        serve_forever(args.host, args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
