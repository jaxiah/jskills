@echo off
setlocal

if "%~1"=="" (
  echo Usage: %~nx0 AGENT_NAME
  echo Example: %~nx0 codex
  exit /b 1
)

set "SCRIPT_DIR=%~dp0"
set "AGENT=%~1"
set "HUMAN_TARGET=%SCRIPT_DIR%humansay.cmd"
set "AGENT_TARGET=%SCRIPT_DIR%agentturn.cmd"

echo %AGENT%| findstr /R "^[a-z0-9][a-z0-9_-]*$" >nul
if errorlevel 1 (
  echo Error: AGENT_NAME must match [a-z0-9][a-z0-9_-]*
  exit /b 1
)

(
  echo @echo off
  echo python "%SCRIPT_DIR%humansay.py" --root "%%CD%%" %%*
) > "%HUMAN_TARGET%"

(
  echo @echo off
  echo python "%SCRIPT_DIR%agentturn.py" --root "%%CD%%" --agent "%AGENT%" %%*
) > "%AGENT_TARGET%"

echo Generated "%HUMAN_TARGET%"
echo Generated "%AGENT_TARGET%" for agent "%AGENT%"
