import xml.etree.ElementTree as ET
from src.document import Document

filename = 'tests/data/input.xml'
docname = 'Dummy name'
format = 'colmep'
d = Document.create_from_nonstandard_file(filename, docname, format)
# print(d.tag)
d.transform_tokenise_sentences()
# NB make sure to update spellings before adding text to sentences
d.transform_remove_asterisks()
d.transform_add_text_to_sentences()
# get sentences
sents = d.get_sentences_as_text()
# for s in sents:
#     print(s, '\n')
# print the first part of the XML to check
# xml = d.to_xml_string(indent=4)
# print(xml[:5000])
# print('Sentences :', d.get_sentence_count())
e = d.get_underlying_element()
l = list(e.iter('w'))
print(l[:10])
print('Words     :', d.get_word_count())
# print('Longest   :', d.get_longest_sentence())
# print('Shortest  :', d.get_shortest_sentence())
# print('Average   :', d.get_average_sentence_length())