from corpusparser.corpus_element import CorpusElement
import xml.etree.ElementTree as ET   

class Corpus(CorpusElement):

    # a lightweight container for a collection of documents
    # its primary purpose is to allow functions such as word frequency to be
    # applied across multiple documents

    # initialise with the provided underlying element
    def __init__(self, element: ET.Element) -> None:
        self.e = element
        self.e.tag = 'corpus'

    ##############################################################################
    # Object creation methods - overridden from CorpusParser

    # create an empty corpus
    def create_new():
        new_e = ET.Element('corpus')
        return Corpus(new_e)