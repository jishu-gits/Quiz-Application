# Quiz Generator Desktop — Silent Ollama Installer
# ==================================================
# Downloads and installs Ollama for Windows silently.
# Called by startup_manager.pyw when Ollama is not detected.

$ErrorActionPreference = "Stop"

$ollamaUrl = "https://ollama.com/download/OllamaSetup.exe"
$tempDir = Join-Path $env:TEMP "QuizGeneratorSetup"
$installerPath = Join-Path $tempDir "OllamaSetup.exe"

try {
    Write-Host "Creating temp directory..."
    New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

    Write-Host "Downloading Ollama installer from $ollamaUrl..."
    # Use BITS for reliable download, fallback to WebClient
    try {
        Start-BitsTransfer -Source $ollamaUrl -Destination $installerPath -ErrorAction Stop
    } catch {
        Write-Host "BITS transfer failed, falling back to WebClient..."
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($ollamaUrl, $installerPath)
    }

    if (-not (Test-Path $installerPath)) {
        Write-Error "Download failed — installer not found at $installerPath"
        exit 1
    }

    $fileSize = (Get-Item $installerPath).Length
    Write-Host "Downloaded successfully ($fileSize bytes)"

    Write-Host "Running Ollama installer silently..."
    $process = Start-Process -FilePath $installerPath `
        -ArgumentList "/SILENT", "/NORESTART", "/SUPPRESSMSGBOXES" `
        -Wait -PassThru -NoNewWindow

    if ($process.ExitCode -eq 0) {
        Write-Host "Ollama installed successfully (exit code 0)"
    } else {
        Write-Host "Ollama installer exited with code $($process.ExitCode)"
    }

    # Refresh PATH for current session
    $machinePath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
    $userPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
    $env:Path = "$machinePath;$userPath"

    # Verify installation
    $ollamaExe = Get-Command ollama -ErrorAction SilentlyContinue
    if ($ollamaExe) {
        Write-Host "Verification passed: ollama found at $($ollamaExe.Source)"
        exit 0
    } else {
        Write-Host "WARNING: ollama not found in PATH after installation"
        # Check common install locations
        $commonPaths = @(
            "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe",
            "$env:ProgramFiles\Ollama\ollama.exe"
        )
        foreach ($p in $commonPaths) {
            if (Test-Path $p) {
                Write-Host "Found ollama at: $p"
                exit 0
            }
        }
        exit 1
    }
} catch {
    Write-Error "Ollama installation failed: $_"
    exit 1
} finally {
    # Cleanup temp installer
    if (Test-Path $tempDir) {
        Remove-Item -Recurse -Force $tempDir -ErrorAction SilentlyContinue
    }
}
