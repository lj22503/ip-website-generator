@echo off
cd /d C:\Users\lj225\Hermes\workspace\projects\ip-website-generator\skill
python capture_smoke.py > smoke_out.txt 2>&1
echo Exit code: %ERRORLEVEL% >> smoke_out.txt
type smoke_out.txt