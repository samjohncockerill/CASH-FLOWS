# Carga el entorno del proyecto cashflows en la sesion actual de PowerShell.
# Uso:
#   . .\run.ps1            # cargar (notese el punto inicial: dot-sourcing)
#   cashflows npv --rate 0.1 -1000 400 400 400
#   cashflows irr -1000 500 500 500
#   cashflows payback -1000 400 400 400
#   cf-test                # corre pytest

$script:RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = Join-Path $script:RepoRoot "src"

function global:cashflows {
    python -m cashflows.cli @args
}

function global:cf-test {
    python -m pytest @args
}

Write-Host "cashflows env cargado." -ForegroundColor Green
Write-Host "  PYTHONPATH = $env:PYTHONPATH"
Write-Host "  comandos:    cashflows <npv|irr|payback> ...   |   cf-test"
Write-Host ""
Write-Host "Demo:" -ForegroundColor Cyan
Write-Host "  cashflows npv --rate 0.1 -1000 400 400 400"
Write-Host "  cashflows irr -1000 500 500 500"
Write-Host "  cashflows payback -1000 400 400 400"
