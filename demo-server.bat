@echo off
cd /d "%~dp0"
set PORT=9080
echo ==============================================
echo   EL MANANERO DEPORTES - Demo (Cloudflare)
echo   Puerto local: %PORT%
echo ==============================================
echo.
python demo.py
echo.
echo (La ventana puede cerrarse)
pause
