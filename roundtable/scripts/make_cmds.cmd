@echo off
setlocal

if "%~1"=="" (
  echo Usage: %~nx0 AGENT_NAME
  echo Example: %~nx0 codex
  exit /b 1
)

set "SCRIPT_DIR=%~dp0"
set "AGENT=%~1"
set "AGENT_TARGET=%SCRIPT_DIR%agentturn.cmd"
set "TUI_TARGET=%CD%\roundtable.cmd"

echo %AGENT%| findstr /R "^[a-z0-9][a-z0-9_-]*$" >nul
if errorlevel 1 (
  echo Error: AGENT_NAME must match [a-z0-9][a-z0-9_-]*
  exit /b 1
)

(
  echo @echo off
  echo python "%SCRIPT_DIR%agentturn.py" --root "%%CD%%" --agent "%AGENT%" %%*
) > "%AGENT_TARGET%"

(
  echo @echo off
  echo setlocal
  echo python -c "import textual, rich" ^>nul 2^>^&1
  echo if errorlevel 1 ^(
  echo     echo [ERROR] The Textual TUI requires additional Python libraries.
  echo     echo Please run: pip install textual rich
  echo     echo.
  echo     pause
  echo     exit /b 1
  echo ^)
  echo python "%SCRIPT_DIR%roundtable.py"
) > "%TUI_TARGET%"

echo Generated "%AGENT_TARGET%" for agent "%AGENT%"
echo Generated "%TUI_TARGET%" in current directory
