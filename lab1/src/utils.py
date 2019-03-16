import re

import regex


def omit_header(text):
    return regex.match(r'.*?(\bArt\b.*)', text, regex.MULTILINE | regex.DOTALL)[1]
