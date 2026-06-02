# Run smoke test and save results
$ErrorActionPreference = "SilentlyContinue"
$outFile = "C:\Users\lj225\Hermes\workspace\projects\ip-website-generator\skill\smoke_results.json"
$errFile = "C:\Users\lj225\Hermes\workspace\projects\ip-website-generator\skill\smoke_err.txt"

# Try to find python
$pythonCmd = $null
foreach ($py in @("python", "python3", "py", "python.exe", "python3.exe")) {
    $resolved = Get-Command $py -ErrorAction SilentlyContinue
    if ($resolved) {
        $pythonCmd = $resolved.Source
        break
    }
}

if (-not $pythonCmd) {
    "No Python found" | Out-File $errFile
    exit 1
}

"$pythonCmd found at $pythonCmd" | Out-File $errFile

# Run the test
$start = Get-Date
$proc = Start-Process -FilePath $pythonCmd -ArgumentList "C:\Users\lj225\Hermes\workspace\projects\ip-website-generator\skill\capture_smoke.py" -NoNewWindow -Wait -PassThru -RedirectStandardOutput $outFile -RedirectStandardError $errFile
$exitCode = $proc.ExitCode
$duration = (Get-Date) - $start

"Exit code: $exitCode" | Out-File $errFile -Append
"Duration: $($duration.TotalSeconds)s" | Out-File $errFile -Append

if (Test-Path $outFile) {
    Get-Content $outFile
}
if (Test-Path $errFile) {
    Get-Content $errFile
}