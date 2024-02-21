import xml.etree.ElementTree as ET
from src.document import Document

filename = 'tests/data/input.xml'
d = Document()
d.import_colmep_format(filename, 'Dummy name')
# print(d.tag)
d.transform_tokenise_sentences()
# NB make sure to update spellings before adding text to sentences
d.transform_remove_asterisks()
d.transform_add_text_to_sentences()
# get sentences
sents = d.get_sentence_text()
for s in sents:
    print(s, '\n')
# print the first part of the XML to check
ET.indent(d, space='  ')
xml = ET.tostring(d, encoding='unicode')
print(xml[:5000])
# print('Sentences :', d.get_sentence_count())
# print('Words     :', d.get_word_count())
# print('Longest   :', d.get_longest_sentence())
# print('Shortest  :', d.get_shortest_sentence())
# print('Average   :', d.get_average_sentence_length())