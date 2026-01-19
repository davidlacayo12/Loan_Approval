# clean.ps1
Write-Host "Cleaning up Python build and cache files from src/ and tests/..." -ForegroundColor Cyan

# Define folders to clean
$folders = @("backend")

foreach ($folder in $folders) {
    if (Test-Path $folder) {
        Write-Host "`nCleaning folder: $folder" -ForegroundColor Yellow

        # Remove __pycache__ directories
        Get-ChildItem -Path $folder -Recurse -Directory -Filter '__pycache__' |
            ForEach-Object {
                Write-Host "Removing directory: $($_.FullName)"
                Remove-Item $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
            }

        # Remove .pyc and .pyo files
        Get-ChildItem -Path $folder -Recurse -Include *.pyc, *.pyo |
            ForEach-Object {
                Write-Host "Removing file: $($_.FullName)"
                Remove-Item $_.FullName -Force -ErrorAction SilentlyContinue
            }

        # Optional: remove test caches (e.g., pytest/mypy/etc.)
        $optionalDirs = @(".pytest_cache", ".mypy_cache", ".hypothesis")
        foreach ($optDir in $optionalDirs) {
            Get-ChildItem -Path $folder -Recurse -Directory -Filter $optDir |
                ForEach-Object {
                    Write-Host "Removing directory: $($_.FullName)"
                    Remove-Item $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
                }
        }
    } else {
        Write-Host "Folder not found: $folder" -ForegroundColor Red
    }
}

Write-Host "`nCleanup complete!" -ForegroundColor Green
