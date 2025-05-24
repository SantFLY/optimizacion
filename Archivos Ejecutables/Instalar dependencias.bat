@echo off
echo Instalando dependencias...
python -m pip install --upgrade pip
pip install -r ../requirements.txt
echo.
echo Dependencias instaladas correctamente!
echo.
pause 