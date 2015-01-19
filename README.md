# Pandoc Plantuml filter

Use plantuml.py as filter in order to make plantuml images from source code in markdown

## Use plantuml filter

>pandoc --filter ./plantuml.py example.txt -o example.html

## Bonus: make cyrillic pdf

>pandoc --filter ./plantuml.py --latex-engine=xelatex --template=template.tex example.txt -o example.pdf
