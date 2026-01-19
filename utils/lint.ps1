# lint.ps1
Write-Host "Running formatters and type checkers on backend/..." -ForegroundColor Cyan

# --- Run Black ---
Write-Host "`nFormatting with Black..." -ForegroundColor Yellow
python -m black backend/

# --- Run isort ---
Write-Host "`nSorting imports with isort..." -ForegroundColor Yellow
python -m isort backend/ --profile black

# --- Run mypy ---
Write-Host "`nType checking with mypy..." -ForegroundColor Yellow
python -m mypy backend/

Write-Host "`nLinting complete!" -ForegroundColor Green
