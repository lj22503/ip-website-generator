"""Run smoke test via Python executable."""
import subprocess
import sys

result = subprocess.run(
    [sys.executable, r'C:\Users\lj225\Hermes\workspace\projects\ip-website-generator\skill\smoke_test.py'],
    capture_output=True,
    text=True,
    timeout=60
)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)