@ECHO OFF
@SET mypath=%~dp0
@SET filepath=%~f1
@SET plantuml=%mypath%plantuml.py
@SET result=%~n1.html
@SET pandoc=%mypath%pandoc.exe

%pandoc% --filter %plantuml% -o %result% %filepath%
