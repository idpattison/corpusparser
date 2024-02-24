from src.corpus_element import CorpusElement
from src.word import Word
import xml.etree.ElementTree as ET   

import benepar, spacy

# gloabl NLP pipe
nlp = None

# Sentence class represents a sentence in the text

class Sentence(CorpusElement):

    # initialise with the provided underlying element
    def __init__(self, element: ET.Element) -> None:
        self.e = element
        self.e.tag = 's'

    ##############################################################################
    # Object creation methods - overridden from CorpusParser

    # create a sentence from an underlying element
    def create_from_element(e: ET.Element):
        return Sentence(e)
    
    # create a sentence from a text string
    def create_from_xml_string(text: str):
        new_e = ET.fromstring(text)
        return Sentence.create_from_element(new_e)
    
    # create a sentence from new
    def create_new():
        new_e = ET.Element('s')
        return Sentence(new_e)

    # create a sentence as a new object in the tree
    def append_new(parent, tag: str):
        new_e = ET.SubElement(parent.get_underlying_element(), tag)
        return Sentence(new_e)
    
    # create a sentence from a specific index in a parent
    def create_from_parent_and_index(parent: CorpusElement, index: int):
        sent_e = parent.get_sentence_element_by_index(index)
        return Sentence.create_from_element(sent_e)
    
    ##############################################################################

    def get_words(self) -> list:
        word_elems = self.get_words_as_elements()
        word_list = []
        for w in word_elems:
            word_list.append(Word.create_from_element(w))
        return word_list
    
    def prepare_parser() -> None:
        benepar.download('benepar_en3')
        nlp = spacy.load('en_core_web_md')
        nlp.add_pipe('benepar', config={'model': 'benepar_en3'})

    def parse():
        doc = nlp("The right plesaunt and goodly historie of the foure sonnes of Aymon the which for the excellent endytyng of it , and for the notable prowes and great vertues that were in them : is no less pleasaunt to rede , then worthy to be knowen of all estates bothe hyghe and lowe .")
        sent = list(doc.sents)[0]
        parse = sent._.parse_string
        items = parse.split(' ')
        for i in items:
            if i.startswith('('):
                if i in ['(S', '(CP', '(IP', '(VP', '(NP', '(PP', '(ADJP', '(ADVP', '(CONJP', '(QP', '(DP']:
                print('phrase: ', i)
                else:
                print('pos:    ', i)
            else:
                print('word:   ', i)