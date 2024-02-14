import xml.etree.ElementTree as ET
from src.document import Document
from src.transformers import Transformers

filename = 'tests/data/input.xml'
d = Document()
d.import_colmep_format(filename, 'Dummy name')
print(d.tag)
Transformers.transform_tokenise_sentences(d)
# print the first part of the XML to check
ET.indent(d, space='  ')
xml = ET.tostring(d, encoding='unicode')
print(xml[:5000])