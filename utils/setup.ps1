# setup.ps1
Write-Host "Setting up Python virtual environment..." -ForegroundColor Cyan

# Create virtual environment (if not already created)
if (-Not (Test-Path "venv")) {
    python -m venv venv
    Write-Host "Virtual environment created."
} else {
    Write-Host "Virtual environment already exists. Skipping creation."
}

# Activate virtual environment
. .\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install uv (if not already installed)
pip show uv > $null
if ($LASTEXITCODE -ne 0) {
    pip install uv
    Write-Host "Installed uv."
} else {
    Write-Host "uv already installed."
}

# Install all requirements via uv
$requirementFiles = @(
    "requirements/build.txt",
    "requirements/dev.txt",
    "requirements/test.txt",
    "requirements/project.txt"
)

# Create an array of "-r <file>" strings
$requirementArgs = $requirementFiles | ForEach-Object { "-r"; $_ }

# Now run uv pip install with the array splatted as arguments
uv pip install @requirementArgs

# Install mypy stubs that are missing
mypy --install-types

Write-Host ""
Write-Host "Environment setup complete." -ForegroundColor Green
