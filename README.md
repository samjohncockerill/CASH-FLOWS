# CASH-FLOWS

Analizador de flujos de caja e inversiones, en Python puro **sin dependencias**.
Funciona como CLI con graficos ASCII a color **y** como app web local con
graficos interactivos (Chart.js desde CDN, no requiere instalacion).

## Funcionalidades

| Comando | Que hace |
|---|---|
| `serve` | **Lanza la app web local** (http://127.0.0.1:8000) |
| `analyze` | Reporte CLI completo: grafico de flujos + NPV/IRR/MIRR/Payback/PI + veredicto |
| `loan` | Cuadro de amortizacion de prestamo o hipoteca con resumen |
| `sensitivity` | Grafico de NPV vs tasa de descuento (curva de sensibilidad) |
| `npv`, `irr`, `payback` | Comandos rapidos para un solo numero |

## Estructura

```
src/cashflows/
  core.py             NPV, IRR, MIRR, payback, indice de rentabilidad
  loan.py             amortizacion (PMT) y reporte
  charts.py           graficos ASCII (barras horizontales, line chart)
  ui.py               colores ANSI y cajas
  analyzer.py         reporte completo de inversion
  web.py              servidor HTTP stdlib + endpoints JSON
  static/index.html   SPA con 3 pestanas (analisis / prestamo / sensibilidad)
  cli.py              linea de comandos
tests/                26 tests con pytest
pyproject.toml
run.ps1               bootstrap PowerShell (cashflows, cf-test, cf-web)
```

## Ramas

- `main` — version estable
- `develop` — integracion
- `feature/python-setup` — rama de feature

## Uso rapido

```powershell
# 1. Cargar entorno (una vez por sesion)
. .\run.ps1

# 2. Web app: el camino mas chulo
cf-web -Open                   # abre en el navegador en http://127.0.0.1:8000

# 3. CLI: analisis completo
cashflows analyze --rate 0.10 -1000 400 400 400 200

# 4. CLI: hipoteca de 200k al 4.5% a 30 anios
cashflows loan --principal 200000 --rate 0.045 --years 30

# 5. Sensibilidad NPV vs tasa
cashflows sensitivity --from 0 --to 0.30 --step 0.03 -1000 400 400 400 200

# 6. Tests
cf-test
```

## App web

Tres pestanas:

1. **Analisis de inversion**: introduces flujos (con + / x para anadir/quitar
   periodos), tasa de descuento, y obtienes barras coloreadas, las 5 metricas
   y un veredicto **INVERTIR / RECHAZAR** con razones.
2. **Prestamo / Hipoteca**: capital + tasa + anios -> cuota mensual, total
   intereses, % sobrecoste, grafico apilado capital-vs-interes a lo largo del
   tiempo, y cuadro de amortizacion (primeros + ultimos meses).
3. **Sensibilidad**: como cambia el NPV cuando varia la tasa de descuento,
   con marcador del IRR (cruce con NPV=0).

API JSON disponible en `/api/analyze`, `/api/loan`, `/api/sensitivity`.

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
