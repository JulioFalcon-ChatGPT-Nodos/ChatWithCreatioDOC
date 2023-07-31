@Echo Off
Rem Crea entorno virtual usando Python 3.9
c:\JulioFalcon\OneDriveNodos\OneDrive\OpenAI\Python\Python39\python -m venv 01_chat39

Rem Lo activa
.\01_chat39\Scripts\activate

REM Actualiza PIP
.\01_chat39\scripts\python.exe -m pip install --upgrade pip

REM Instala requerimientos
.\01_chat39\scripts\pip install -r requirements.txt

Rem Ejecuta VSCode
code .
