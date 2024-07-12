import xml.etree.ElementTree as ET
import corpusparser

from corpusparser import Document

filename = 'tests/data/input.xml'
format = 'colmep'
spellings = 'tests/data/spellings.json'

d = Document.create_from_nonstandard_file(filename, format)
d.transform_tokenise_sentences()
d.update_spellings_from_file(spellings)
d.transform_add_convenience_text_to_sentences()
# d.transform_parse(add_parse_string=True, restructure=True)

d.to_xml_file('tests/data/sandbox-output.xml', indent=2)
