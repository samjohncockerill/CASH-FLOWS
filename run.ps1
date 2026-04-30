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

function global:cf-web {
    param([int]$Port = 8000, [switch]$Open)
    $extra = @()
    if ($Open) { $extra += "--open" }
    python -m cashflows.cli serve --port $Port @extra
}

Write-Host "cashflows env cargado." -ForegroundColor Green
Write-Host "  PYTHONPATH = $env:PYTHONPATH"
Write-Host "  comandos:    cashflows <analyze|loan|sensitivity|...> ...   |   cf-test   |   cf-web -Open"
Write-Host ""
Write-Host "Demo:" -ForegroundColor Cyan
Write-Host "  cashflows analyze --rate 0.10 -1000 400 400 400 200"
Write-Host "  cashflows loan --principal 200000 --rate 0.045 --years 30"
Write-Host "  cashflows sensitivity --from 0 --to 0.30 --step 0.03 -1000 400 400 400 200"
Write-Host "  cf-web -Open                  # abre la app web en el navegador"
