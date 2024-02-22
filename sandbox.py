import xml.etree.ElementTree as ET
from src.document import Document
from src.sentence import Sentence

filename = 'tests/data/input.xml'
docname = 'Dummy name'
format = 'colmep'
d = Document.create_from_nonstandard_file(filename, docname, format)
# print(d.tag)
d.transform_tokenise_sentences()
# NB make sure to update spellings before adding text to sentences
d.transform_remove_asterisks()
d.transform_v_to_u()
d.transform_u_to_v()
d.transform_ye_caret_to_the()
d.transform_add_convenience_text_to_sentences()
# get sentences
# sents = d.get_sentences_as_text_list()
# for s in sents:
#     print(s, '\n')
# print the first part of the XML to check
# xml = d.to_xml_string(indent=4)
# print(xml[:5000])
# print('Sentences :', d.get_sentence_count())
# sent_e = d.get_sentences_as_elements()
# s = Sentence.create_from_element(sent_e[0])
# t = s.get_attribute('conv-text')
# print(t)
# e = d.get_underlying_element()
# l = list(e.iter('w'))
# print(l[:10])
print('Words     :', d.get_word_count())
print('Longest   :', d.get_longest_sentence())
print('Shortest  :', d.get_shortest_sentence())
print('Average   :', d.get_average_sentence_length())
print(d.word_frequency_starts_with('w'))
# print(d.word_frequency_contains_punctuation())
print(d.get_xml_tags())

sents = d.get_sentences_as_elements()
# check this is the right size
print(len(sents))
# check we can create Sentence objects
s = Sentence.create_from_element(sents[2])
t = s.get_attribute('conv-text')
print(t[:18])

# write to file
# out_file = 'tests/data/output.xml'
# d.to_xml_file(out_file, indent=2)

conc = d.concordance_in(['which', 'whiche', 'whyche'], separator='@')
for c in conc:
    print(c)