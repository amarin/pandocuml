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

logging.basicConfig(format="%(asctime) %(func)s:%(lineno)s %(message)s")
# Logging
_l = logging.getLogger(__name__)
_l.setLevel(logging.ERROR)
debug, info, warning, error, critical = _l.debug, _l.info, _l.warning, _l.error, _l.critical
info("Filter plantuml started")

# direct link
plantuml_path = os.path.dirname(os.path.realpath(sys.argv[0]))
plantuml_jar = os.path.join(plantuml_path, "plantuml.jar")

plantuml_config = '%s/plantuml.conf' % plantuml_path
plantuml_options = '-config "%s" -charset utf8' % plantuml_config

# create empty config
if not os.path.exists(plantuml_config):
    with open(plantuml_config, 'w') as plantuml_config_file:
        plantuml_config_file.write('')


warning("Using plantuml %s with options %s", plantuml_jar, plantuml_options)


def sha1(x):
    # make hash of string x
    return hashlib.sha1(x).hexdigest()


def plantuml(key, value, format, meta):
    if key == 'CodeBlock':
        [[ident, classes, keyvals], plantuml_code] = value
        caption = "caption"
        if "plantuml" in classes or plantuml_code.startswith(PLANTUML_PREFIX):
            warning("Come into plantuml block")
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
            img_alt = Str(caption)
            img_src = imagedir + '/' + filename + '.png'
            debug("Image path %s" % img_src)

            img_title = ""
            img_params = ["", [], []]
            img = Image(img_params, [img_alt], [img_src, img_title])

            #os.remove(img_src)
            if not os.path.exists(img_src):
                info("Image file %s not exists, so source is new or changed, process code" % img_src)
                try:
                    uml = imagedir + '/' + filename + '.txt'
                    if not os.path.isfile(img_src):
                        try:
                            os.makedirs(imagedir)
                            info("Created directory %s", imagedir)
                        except OSError as exc:
                            error("Failed create image dir: %s", exc)
                            exit(64)

                    debug("Will create image %s\n" % img_src)
                    with open(uml, 'w') as plantuml_source:
                        debug("Saving plantuml source in %s" % plantuml_source)
                        plantuml_source.write(plantuml_code)
                        info("Saved plantumlcode at separate file %s", uml)
                    info("Process plantuml")
                    execute_plantuml = "java -jar {} {} {}".format(plantuml_jar, plantuml_options, uml)
                    info('Calling {}'.format(execute_plantuml))
                    os.system(execute_plantuml)
                    info("Plantuml processing done")
                except Exception as exc:
                    error(exc)
                    exit(64)
            else:
                info("Image exists, do nothing")

            warning("Finishing processing")

            debug("Image AST: %s" % img)
            para = Para([img])
            debug("Para: %s" % para)
            return para

if __name__ == "__main__":
    toJSONFilter(plantuml)
