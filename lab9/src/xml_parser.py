import xml.etree.ElementTree as ET


def parse_groups(grp):
    word = [[_x.text for _x in x if _x.tag == 'base'][0] for x in grp if x.tag == 'lex'][0]
    groups = [(x.attrib['chan'], int(x.text)) for x in grp if x.tag == 'ann' and x.attrib['chan'] != '']
    return word, groups


def parse_xml(data):
    doc = ET.fromstring(data)
    chunks = [x for x in doc]
    sentences = [[x for x in c] for c in chunks]
    tokens = [[[parse_groups([c for c in t]) for t in x if t.tag == 'tok'] for x in s] for s in sentences]
    return tokens
