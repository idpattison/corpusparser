import xml.etree.ElementTree as ET
import corpusparser

from corpusparser import Document
from corpusparser import Corpus

format = 'colmep'

works = [
    { "title": "Arthur of Little Britain",           "year": 1530, "source": "French", "region": "EM" },
    { "title": "Caxton's Blanchardyn and Eglantine", "year": 1489, "source": "French", "region": "LO" },
    { "title": "Caxton's Charles the Grete",         "year": 1485, "source": "French", "region": "LO" },
    { "title": "Caxton's Eneydos",                   "year": 1490, "source": "French", "region": "LO" },
    { "title": "Caxton's Four Sons of Aymon",        "year": 1485, "source": "French", "region": "LO" },
    { "title": "Caxton's Godeffroy of Boloyne",      "year": 1481, "source": "French", "region": "LO" },
    { "title": "Caxton's History of Jason",          "year": 1477, "source": "French", "region": "LO" },
    { "title": "Caxton's Paris and Vienne",          "year": 1485, "source": "French", "region": "LO" },
    { "title": "Caxton's Recuyell",                  "year": 1472, "source": "French", "region": "LO" },
    { "title": "Dublin Alexander Epitome",           "year": 1450, "source": "French", "region": "NO" },
    { "title": "Huon of Bordeaux",                   "year": 1525, "source": "French", "region": "EM" },
    { "title": "Joseph of Arimathie Fragment",       "year": 1510, "source": "Latin",  "region": "LO" },
    { "title": "King Apollyn",                       "year": 1508, "source": "French", "region": "LO" },
    { "title": "King Ponthus and the Fair Sidone",   "year": 1435, "source": "French", "region": "NO" },
    { "title": "Malory 1 Arthur",                    "year": 1465, "source": "French", "region": "WA" },
    { "title": "Malory 2 War against Romans",        "year": 1466, "source": "French", "region": "WA" },
    { "title": "Malory 3 Sir Launcelot",             "year": 1467, "source": "French", "region": "WA" },
    { "title": "Malory 4 Sir Gareth of Orkney",      "year": 1468, "source": "French", "region": "WA" },
    { "title": "Malory 5 Sir Tristram",              "year": 1469, "source": "French", "region": "WA" },
    { "title": "Malory 6 The Holy Grail",            "year": 1470, "source": "French", "region": "WA" },
    { "title": "Malory 7 Launcelot and Guinevere",   "year": 1471, "source": "French", "region": "WA" },
    { "title": "Malory 8 Morte Arthur",              "year": 1471, "source": "French", "region": "WA" },
    { "title": "Melusine",                           "year": 1500, "source": "French", "region": "EM" },
    { "title": "Oliver of Castille",                 "year": 1515, "source": "French", "region": "EM" },
    { "title": "Pierre of Provence Fragment",        "year": 1490, "source": "French", "region": "EM" },
    { "title": "Prose Alexander",                    "year": 1420, "source": "Latin",  "region": "NO" },
    { "title": "Prose Ipomedon",                     "year": 1450, "source": "French", "region": "NW" },
    { "title": "ProseMerlin",                        "year": 1450, "source": "French", "region": "KE" },
    { "title": "Robert the Deuyll",                  "year": 1496, "source": "French", "region": "EM" },
    { "title": "Siege of Jerusalem",                 "year": 1485, "source": "French", "region": "SW" },
    { "title": "Siege of Thebes",                    "year": 1425, "source": "French", "region": "EM" },
    { "title": "Siege of Troy",                      "year": 1425, "source": "French", "region": "EM" },
    { "title": "The Knight of the Swan",             "year": 1510, "source": "French", "region": "EM" },
    { "title": "The Three Kings' Sons",              "year": 1475, "source": "French", "region": "EM" },
    { "title": "Turpine's Story",                    "year": 1455, "source": "Latin",  "region": "WM" },
    { "title": "Valentine and Orson",                "year": 1503, "source": "French", "region": "LO" },
    { "title": "Virgilius",                          "year": 1518, "source": "Dutch",  "region": "LO" },
    { "title": "William of Palerne Fragment",        "year": 1515, "source": "Native", "region": "EM" },
]

# process each work in turn
for work in works:
    print("Adding: ", work["title"])

    # import the document from file
    d = Document.create_from_nonstandard_file('tests/corpus/' + work["title"] + '.xml', format)

    # update the spellings based on the spelling file
    d.update_spellings_from_file('tests/data/spellings.json')

    # split into sentences and number them for referencing
    d.transform_tokenise_sentences(tokenisation_model="period_and_capital")
    d.transform_number_sentences()

    # write the sentences to file
    sents = d.get_sentences_as_text_list(correctedText=True)
    try:
        with open('tests/sentences/' + work["title"] + '.txt', 'w') as f:
            for s in sents:
                f.write(f"{s}\n")
    except IOError:
        print("Error writing file")

    # count the words under study and add to the dictionary
    work["he"] = d.word_count_in(['he', 'He', 'HE', 'hee'], correctedText=True)
    work["him"] = d.word_count_in(['him', 'HIM', 'hym', 'HYM', 'hyme'], correctedText=True)
    work["ye"] = d.word_count_in(['ye', 'Ye', 'YE', 'yee', 'yie', 'ȝe', 'Ȝe', 'ȝee', 'Ȝee'], correctedText=True)
    work["you"] = d.word_count_in(['you', 'You', 'YOu', 'yow', 'yeu', 'ȝou', 'ȝow'], correctedText=True)

    # \Wye\W|\WYe\W|\WYE\W|\Wyee\W|\Wyie\W|\Wȝe\W|\WȜe\W|\Wȝee\W|\WȜee\W

# now write out the results to CSV
try:
    with open('tests/data/sandbox5-output.txt', 'w') as f:
        f.write("Title,Year,Source,Region,He,Him,Ye,You\n")
        for work in works:
            f.write(work["title"] + ',' + 
                    str(work["year"]) + ',' +
                    work["source"] + ',' +
                    work["region"] + ',' +
                    str(work["he"]) + ',' +
                    str(work["him"]) + ',' +
                    str(work["ye"]) + ',' +
                    str(work["you"]) + ',' +
                    '\n')
            
except IOError:
    print("Error writing file")
