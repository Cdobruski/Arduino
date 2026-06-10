@echo off
chcp 65001 > nul
echo ============================================
echo   Build - Dilemas Eticos
echo ============================================
echo.

echo [1/3] Instalando dependencias...
pip install PyQt5 pyserial pyinstaller
if errorlevel 1 (
    echo ERRO: pip nao encontrado. Certifique-se de que o Python esta no PATH.
    pause
    exit /b 1
)

echo.
echo [2/3] Gerando executavel...
pyinstaller ^
  --onefile ^
  --windowed ^
  --name "DilemasEticos" ^
  --hidden-import serial.serialwin32 ^
  --hidden-import serial.serialutil ^
  main.py

if errorlevel 1 (
    echo ERRO: PyInstaller falhou. Verifique os logs acima.
    pause
    exit /b 1
)

echo.
echo [3/3] Copiando config.json para dist\...
copy /Y config.json dist\config.json

echo.
echo ============================================
echo   PRONTO!
echo   Executavel: dist\DilemasEticos.exe
echo.
echo   Para trocar a porta COM, edite:
echo   dist\config.json  ^(serial_port^)
echo ============================================
pause
