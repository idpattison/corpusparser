from src.corpus_element import CorpusElement
import xml.etree.ElementTree as ET   

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

