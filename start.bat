echo off
title Iniciando MONL...
cd /d %~dp0

echo ===================================================
echo Verificando dependencias e instalando se necessario...
echo ===================================================

python -m pip install -r requirements.txt

echo.
echo ===================================================
echo Tudo pronto! Iniciando o programa...
echo ===================================================

python main.py

pause