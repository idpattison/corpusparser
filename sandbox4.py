import xml.etree.ElementTree as ET
import corpusparser

from corpusparser import Document
from corpusparser import Corpus

format = 'colmep'

filenames = [
    "Arthur of Little Britain",
    "Caxton's Blanchardyn and Eglantine",
    "Caxton's Charles the Grete",
    "Caxton's Eneydos",
    "Caxton's Four Sons of Aymon",
    "Caxton's Godeffroy of Boloyne",
    "Caxton's History of Jason",
    "Caxton's Paris and Vienne",
    "Caxton's Recuyell",
    "Dublin Alexander Epitome",
    "Huon of Bordeaux",
    "Joseph of Arimathie Fragment",
    "King Apollyn",
    "King Ponthus and the Fair Sidone",
    "Malory 1 Arthur",
    "Malory 2 War against Romans",
    "Malory 3 Sir Launcelot",
    "Malory 4 Sir Gareth of Orkney",
    "Malory 5 Sir Tristram",
    "Malory 6 The Holy Grail",
    "Malory 7 Launcelot and Guinevere",
    "Malory 8 Morte Arthur",
    "Melusine",
    "Oliver of Castille",
    "Pierre of Provence Fragment",
    "Prose Alexander",
    "Prose Ipomedon",
    "ProseMerlin",
    "Robert the Deuyll",
    "Siege of Jerusalem",
    "Siege of Thebes",
    "Siege of Troy",
    "The Knight of the Swan",
    "The Three Kings' Sons",
    "Turpine's Story",
    "Valentine and Orson",
    "Virgilius",
    "William of Palerne Fragment",
]

c = Corpus.create_new()

for filename in filenames:
    print("Adding: ", filename)
    d = Document.create_from_nonstandard_file('tests/corpus/' + filename + '.xml', format)
    d.add_to_corpus(c)

c.print_info()

c.update_spellings_from_file('tests/data/spellings.json')

wf = c.word_frequency(correctedText=True)
try:
    with open('tests/data/word_frequency.txt', 'w') as f:
        for word, freq in wf.items():
            f.write(word + '#' + str(freq) + '\n')
except IOError:
    print("Error writing file")
