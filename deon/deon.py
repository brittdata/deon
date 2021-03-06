import os
from pathlib import Path

import xerox

from .formats import EXTENSIONS, FORMATS
from .parser import Checklist

DEFAULT_CHECKLIST = Path(__file__).parent / 'assets' / 'checklist.yml'

CHECKLIST_FILE = Path(os.environ.get('ETHICS_CHECKLIST', DEFAULT_CHECKLIST))


class ExtensionException(Exception):
    pass


class FormatException(Exception):
    pass


def create(checklist, output_format, output, clipboard, overwrite):
    # load checklist
    cl_path = Path(checklist) if checklist else DEFAULT_CHECKLIST
    cl = Checklist.read(cl_path)

    output = Path(output) if output else None

    # output extension is given priority if differing format is included
    if output:
        # get format by file extension
        ext = output.suffix.lower()
        if ext in EXTENSIONS.keys():
            output_format = EXTENSIONS[ext]
        else:
            raise ExtensionException(ext)
    elif output_format:
        if output_format not in FORMATS:
            raise FormatException(output_format)
    else:
        output_format = 'markdown'

    template = FORMATS[output_format](cl)

    # write output or print to stdout
    if output:
        template.write(output, overwrite=overwrite)
    elif clipboard:
        xerox.copy(str(template.render()))
    else:
        return template.render()
