# About

It's a simple wrapper to extend [Pandoc](http://pandoc.org/) with [Plantuml](plantuml.com) fragments support.

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

## Wrapper

There is wrapper to easier call pandoc and convert any document with plantumlfilter

    >2ext <source.md> <extension> # it will produce <source.extension> with pandoc && possibly plantuml

*Note*: for pdf extension it set additional parameters as described in Bonus para


## Installation

0. install pandoc (see [Pandoc installation)](http://pandoc.org/installing.html))
1. clone source
2. pip install -r requirements.txt
3. change plantuml_jar = "/usr/local/bin/plantuml.jar" to your location

## Bonus: make cyrillic pdf
To create pdf you have to install latex engine first. The easiest to install was xelatext for me.
You can use any you likes.
>pandoc --filter ./plantuml.py --latex-engine=xelatex --template=template.tex example.txt -o example.pdf

