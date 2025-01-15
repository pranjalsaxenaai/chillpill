# Step 1: Define the virtual environment directory name
$venvDir = "venv"

# Step 2: Check if the virtual environment already exists
if (!(Test-Path -Path $venvDir)) {
    Write-Host "Creating virtual environment in $venvDir..."
    python -m venv $venvDir
} else {
    Write-Host "Virtual environment already exists in $venvDir."
}

# Step 3: Activate the virtual environment
Write-Host "Activating virtual environment..."
& .\$venvDir\Scripts\Activate.ps1

# Step 4: Install dependencies
if (Test-Path -Path "requirements.txt") {
    Write-Host "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
} else {
    Write-Host "requirements.txt not found. Please ensure it exists in the current directory."
}

# Step 5: Successful Prompt
Write-Host "Setup completed. Virtual environment ready."