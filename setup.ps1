Write-Host "Installing ffmpeg via Chocolatey..."

choco install ffmpeg -y

Write-Host "Installing Python dependencies..."

pip install -r requirements.txt

Write-Host "Installing Playwright browsers..."

playwright install

Write-Host "Done!"