#!/usr/bin/env python

"""
Pandoc filter to process code blocks with class "graphviz" into
graphviz-generated images.
"""

import hashlib
import os
import sys
from pandocfilters import toJSONFilter, Str, Para, Image

plantuml_jar = "/usr/local/bin/plantuml.jar"
plantuml_options = "-charset utf8"


def sha1(x):
    return hashlib.sha1(x).hexdigest()

imagedir = "images"
PLANTUML_PREFIX = '@startuml'
PLANTUML_SUFFIX = '@enduml'


def plantuml(key, value, format, meta):
    if key == 'CodeBlock':
        [[ident, classes, keyvals], plantuml_code] = value
        caption = "caption"
        if "plantuml" in classes or plantuml_code.startswith(PLANTUML_PREFIX):
            # prefix with @staruml if not found
            if not plantuml_code.startswith(PLANTUML_PREFIX):
                plantuml_code = '{}\n{}'.format(
                    PLANTUML_PREFIX,
                    plantuml_code
                )

            if not plantuml_code.endswith(PLANTUML_SUFFIX):
                plantuml_code = '{}\n{}'.format(
                    plantuml_code,
                    PLANTUML_SUFFIX
                )

            filename = sha1(plantuml_code)
            filetype = "png"
            alt = Str(caption)
            src = imagedir + '/' + filename + '.png'
            if not os.path.exists(src):
                uml = imagedir + '/' + filename + '.txt'
                if not os.path.isfile(src):
                    try:
                        os.mkdir(imagedir)
                        sys.stderr.write(
                            'Created directory ' + imagedir + '\n')
                    except OSError:
                        pass

                sys.stderr.write('Created image ' + src + '\n')
                with open(uml, 'w') as plantuml_source:
                    plantuml_source.write(plantuml_code)
                os.system(
                    "java -jar {} {} {}".format(
                        plantuml_jar,
                        plantuml_options,
                        uml
                    )
                )

            tit = ""
            return Para([Image([alt], [src, tit])])

if __name__ == "__main__":
    toJSONFilter(plantuml)
