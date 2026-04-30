# CASH-FLOWS

Pequena libreria de prueba en Python para calculos basicos de flujos de caja:

- `npv(rate, cashflows)` — Valor Presente Neto
- `irr(cashflows)` — Tasa Interna de Retorno (Newton-Raphson)
- `payback_period(cashflows)` — Periodo de recuperacion

## Estructura

```
src/cashflows/   # codigo fuente del paquete
tests/           # pruebas con pytest
pyproject.toml   # configuracion de empaquetado y pytest
```

## Ramas

- `main` — version estable
- `develop` — integracion
- `feature/python-setup` — rama de feature usada para el setup inicial

## Uso rapido

```bash
pip install -e ".[dev]"
pytest
cashflows npv --rate 0.1 -1000 400 400 400
cashflows irr -1000 500 500 500
cashflows payback -1000 400 400 400
```
