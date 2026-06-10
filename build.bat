@echo off
chcp 65001 > nul
echo ============================================
echo   Build - Dilemas Eticos
echo ============================================
echo.

echo Verificando dependencias...
pip show pyinstaller > nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install PyQt5 pyserial pyinstaller
    if errorlevel 1 (
        echo ERRO: pip nao encontrado. Certifique-se de que o Python esta no PATH.
        pause
        exit /b 1
    )
) else (
    echo Dependencias ja instaladas. Pulando instalacao.
)

echo.
echo Gerando executavel...
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
echo Copiando config.json...
copy /Y config.json dist\config.json

echo.
echo ============================================
echo   PRONTO!
echo   Executavel: dist\DilemasEticos.exe
echo.
echo   Para trocar a porta COM, edite:
echo   dist\config.json  (serial_port)
echo ============================================
pause
