# Pandoc Plantuml filter

Use plantuml.py as filter in order to make plantuml images from source code in markdown.
It uses local copy of plantuml.jar to produce images of different plantuml types.
 
Source of plantuml can be included this way:

	```
	@startuml
	<plantuml code>
	@enduml
	```

or, you can define block style in header too, even without @startuml prefix:

	```plantuml
	<plantuml code>
	```

## Use plantuml filter

>pandoc --filter ./plantuml.py example.txt -o example.html

## Installation

1. clone source
2. pip install pandocfilters
3. change plantuml_jar = "/usr/local/bin/plantuml.jar" to your location

## Bonus: make cyrillic pdf

>pandoc --filter ./plantuml.py --latex-engine=xelatex --template=template.tex example.txt -o example.pdf

