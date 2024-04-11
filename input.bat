@echo off
setlocal

rem Leia o valor do arquivo OpId.txt
set /p matricula=<"C:\Users\mayco\Desktop\FBT_GUI\Opid.txt"

rem Exibe a matrícula lida do arquivo
echo %matricula%

rem Restante do script continua aqui...
