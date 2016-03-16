@ECHO OFF
@SET mypath=%~dp0
@SET filepath=%~f1
@SET plantuml=%mypath%plantuml.py
@SET template=%mypath%template.tex
@SET result=%~n1.pdf

@ECHO "pandoc --filter %plantuml% --latex-engine=xelatex --template=%template% -o %result% %filepath%"
pandoc --latex-engine=xelatex --template="%template%" -o "%result%" "%filepath%"
