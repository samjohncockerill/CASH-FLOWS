# CASH-FLOWS

Analizador de flujos de caja e inversiones, en Python puro (sin dependencias).
Salida en color con graficos ASCII, listo para terminal.

## Funcionalidades

| Comando | Que hace |
|---|---|
| `analyze` | Reporte completo: grafico de flujos + NPV/IRR/MIRR/Payback/PI + veredicto |
| `loan` | Cuadro de amortizacion de prestamo o hipoteca con resumen |
| `sensitivity` | Grafico de NPV vs tasa de descuento (curva de sensibilidad) |
| `npv`, `irr`, `payback` | Comandos rapidos para un solo numero |

## Estructura

```
src/cashflows/
  core.py       NPV, IRR, MIRR, payback, indice de rentabilidad
  loan.py       amortizacion (PMT) y reporte
  charts.py     graficos ASCII (barras horizontales, line chart)
  ui.py         colores ANSI y cajas
  analyzer.py   reporte completo de inversion
  cli.py        linea de comandos
tests/          21 tests con pytest
pyproject.toml
run.ps1         bootstrap para PowerShell
```

## Ramas

- `main` — version estable
- `develop` — integracion
- `feature/python-setup` — rama de feature

## Uso

```powershell
# 1. Cargar entorno (una vez por sesion)
. .\run.ps1

# 2. Analisis completo de una inversion
cashflows analyze --rate 0.10 -1000 400 400 400 200

# 3. Hipoteca de 200k al 4.5% a 30 anos
cashflows loan --principal 200000 --rate 0.045 --years 30

# 4. Como cambia el NPV con la tasa de descuento
cashflows sensitivity --from 0 --to 0.30 --step 0.03 -1000 400 400 400 200

# 5. Tests
cf-test
```

## API en Python

```python
from cashflows import npv, irr, mirr, payback_period, profitability_index, amortize

npv(0.10, [-1000, 400, 400, 400])         # -> -5.26
irr([-1000, 500, 500, 500])                # -> 0.2337
mirr([-1000, 200, 300, 400, 500], 0.1, 0.1)# -> 0.1192
profitability_index(0.10, [-1000, 400, 400, 400])  # -> 0.9947
payback_period([-1000, 400, 400, 400])     # -> 2.5

loan = amortize(200_000, 0.045, 30)
print(loan.monthly_payment, loan.total_interest)
```
