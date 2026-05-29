@echo off
powershell -ExecutionPolicy Bypass -File "%~dp0_install_helper.ps1" -jskills "%~dp0."
set "INSTALL_EXIT_CODE=%ERRORLEVEL%"
echo.
echo install.cmd exited with code %INSTALL_EXIT_CODE%.
pause
exit /b %INSTALL_EXIT_CODE%
