import xml.etree.ElementTree as ET
from src.corpusparser import Document

filename = 'tests/data/input.xml'
d = Document()
breakpoint()
d.import_colmep_format(filename, 'Dummy name')
breakpoint()
print(d.tag)
# print the first part of the XML to check
ET.indent(d, space='  ')
xml = ET.tostring(d, encoding='unicode')
print(xml)