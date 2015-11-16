#!env python

"""
Pandoc filter to process code blocks with class "graphviz" into
graphviz-generated images.
"""

import hashlib
import logging
import os
import sys

from pandocfilters import toJSONFilter, Str, Para, Image

imagedir = "images"
logfile = 'plantuml.log'
PLANTUML_PREFIX = '@startuml'
PLANTUML_SUFFIX = '@enduml'

logging.basicConfig(filename=logfile, format="%(asctime) %(func)s:%(lineno)s %(message)s")
# Logging
_l = logging.getLogger(__name__)
_l.setLevel(logging.DEBUG)
debug, info, warning, error, critical = _l.debug, _l.info, _l.warning, _l.error, _l.critical
info("Filter plantuml started")

plantuml_jar = os.path.join("C://", "P279", "plantuml.8029.jar")

plantuml_options = "-charset utf8"
info("Using plantuml %s with options %s", plantuml_jar, plantuml_options)

def sha1(x):
    return hashlib.sha1(x).hexdigest()

def plantuml(key, value, format, meta):
    if key == 'CodeBlock':
        [[ident, classes, keyvals], plantuml_code] = value
        caption = "caption"
        if "plantuml" in classes or plantuml_code.startswith(PLANTUML_PREFIX):
            info("Come into plantuml block")
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
            # filetype = "png"
            alt = Str(caption)
            src = imagedir + '/' + filename + '.png'
            info("Made image path as %s", src)
            if not os.path.exists(src):
                info("Image file not exists, so source is new or changed, process code")
                try:
                    uml = imagedir + '/' + filename + '.txt'
                    if not os.path.isfile(src):
                        try:
                            os.mkdir(imagedir)
                            info("Created directory %s", imagedir)
                        except OSError as exc:
                            error("Error while creating image dir: %s", exc)
                            pass

                    sys.stderr.write('Created image ' + src + '\n')
                    with open(uml, 'w') as plantuml_source:
                        plantuml_source.write(plantuml_code)
                        info("Saved plantumlcode at separate file %s", uml)
                    execute_plantuml = "java -jar {} {} {}".format(plantuml_jar, plantuml_options, uml)
                    info('Calling {}'.format(execute_plantuml))
                    os.system(execute_plantuml)
                    info("Plantuml processing done")
                except Exception as exc:
                    error(exc)
            else:
                info("Image exists, do nothing")
                return Para(plantuml_code)

            tit = ""
            return Para([Image([alt], [src, tit])])

if __name__ == "__main__":
    toJSONFilter(plantuml)
