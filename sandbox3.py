import xml.etree.ElementTree as ET
import corpusparser

from corpusparser import Document
from corpusparser import Corpus

filename1 = 'tests/data/simple-input1.xml'
filename2 = 'tests/data/simple-input2.xml'
format = 'colmep'

c = Corpus.create_new()

d1 = Document.create_from_nonstandard_file(filename1, format)
d1.add_to_corpus(c)
d2 = Document.create_from_nonstandard_file(filename2, format)
d2.add_to_corpus(c)

print('Document 1: ', d1.count_words())
print('Document 2: ', d2.count_words())
print('Combined: ', c.count_words())

c.to_xml_file('tests/data/sandbox3-output.xml', indent=2)
c.print_info()