from corpusparser.document import Document

filename = 'tests/data/Aymon.xml'
format = 'colmep'

# load document from file
d = Document.create_from_nonstandard_file(filename, format)
d.set_name("Caxton's Four Sons of Aymon")
d.set_id('CAXTON-FSOA')

# split into sentences
d.transform_tokenise_sentences(tokenisation_model='period_and_capital')

# perform transforms - spelling, sentence numbering, etc.
d.transform_remove_asterisks()
d.transform_v_to_u()
d.transform_u_to_v()
d.transform_ye_caret_to_the()
d.transform_lbar_to_l()
d.transform_add_original_text_to_sentences()
d.transform_number_sentences()

# get corrected sentences
sents = d.get_sentences_as_text_list(correctedText=True)
# output to file
out_file = 'tests/data/Aymon-sentences-corr.txt'
with open(out_file, 'w') as f:
    for s in sents:
        f.write(s + '\n')

# get sentences
sents = d.get_sentences_as_text_list()
# output to file
out_file = 'tests/data/Aymon-sentences.txt'
with open(out_file, 'w') as f:
    for s in sents:
        f.write(s + '\n')

# get basic info aboout the document
d.print_info()
print(d.word_frequency_starts_with('u'))

# parse sentences
# d.transform_parse(add_parse_string=True, restructure=True, id=d.get_id())
# d.transform_pos_tag(id=d.get_id())

# write xml to file
out_file = 'tests/data/Aymon-output.xml'
d.to_xml_file(out_file, indent=2)

# get parser output and print to file
# out_file = 'tests/data/Aymon-parse.txt'
# with open(out_file, 'w') as f:
#     sents = d.get_sentences()
#     for s in sents:
#         if s.has_attribute('parse'):
#             parse = s.get_attribute('parse')
#             f.write(parse + '\n')
#         else:
#             f.write('No parse for: ' + s.get_attribute('conv-text') + '\n')

# # get POS tags and print to file
# out_file = 'tests/data/Aymon-pos.txt'
# with open(out_file, 'w') as f:
#     sents = d.get_sentences()
#     for s in sents:
#         if s.has_attribute('pos'):
#             pos = s.get_attribute('pos')
#             f.write(pos + '\n')
#         else:
#             f.write('No POS for: ' + s.get_attribute('conv-text') + '\n')


