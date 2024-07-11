import xml.etree.ElementTree as ET
import corpusparser

from corpusparser import Document

filename = 'tests/data/input.xml'
format = 'colmep'
d = Document.create_from_nonstandard_file(filename, format)
d.transform_tokenise_sentences()
d.transform_add_convenience_text_to_sentences()

d.to_xml_file('tests/data/sandbox-output.xml', indent=2)
