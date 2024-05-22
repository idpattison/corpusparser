from corpusparser.corpus_element import CorpusElement
import xml.etree.ElementTree as ET   

# Word class represents a word in the text

class Word(CorpusElement):

    # initialise with the provided underlying element
    def __init__(self, element: ET.Element) -> None:
        self.e = element
        self.e.tag = 'w'

    ##############################################################################
    # Object creation methods - overridden from CorpusParser

    # create a word from an underlying element
    def create_from_element(e: ET.Element):
        return Word(e)
    
    # create a word from a text string
    def create_from_xml_string(text: str):
        new_e = ET.fromstring(text)
        return Word.create_from_element(new_e)
    
    # create a word from new
    def create_new():
        new_e = ET.Element('w')
        return Word(new_e)

    # create a word as a new object in the tree
    def append_new(parent, tag: str):
        new_e = ET.SubElement(parent.get_underlying_element(), tag)
        return Word(new_e)
    
    # create a word from a specific index in a parent
    def create_from_parent_and_index(parent: CorpusElement, index: int):
        word_e = parent.get_word_element_by_index(index)
        return Word.create_from_element(word_e)
    
    # create a word from a specific sentence and word index in a parent
    def create_from_sentence_and_word_index(parent: CorpusElement, sentence_index: int, word_index: int):
        sent_e = parent.get_word_element_by_sentence_and_word_index(sentence_index, word_index)
        return Word.create_from_element(sent_e)

    ##############################################################################