import argparse
from .core import npv, irr, payback_period


def _parse_flows(values):
    return [float(v) for v in values]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="cashflows", description="Calculadora de flujos de caja")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_npv = sub.add_parser("npv", help="Valor Presente Neto")
    p_npv.add_argument("--rate", type=float, required=True)
    p_npv.add_argument("flows", nargs="+")

    p_irr = sub.add_parser("irr", help="Tasa Interna de Retorno")
    p_irr.add_argument("flows", nargs="+")

    p_pb = sub.add_parser("payback", help="Periodo de recuperacion")
    p_pb.add_argument("flows", nargs="+")

    args = parser.parse_args(argv)
    flows = _parse_flows(args.flows)

    if args.cmd == "npv":
        print(f"{npv(args.rate, flows):.6f}")
    elif args.cmd == "irr":
        print(f"{irr(flows):.6f}")
    elif args.cmd == "payback":
        result = payback_period(flows)
        print("never" if result is None else f"{result:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
