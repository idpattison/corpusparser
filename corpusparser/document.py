from corpusparser.corpus_element import CorpusElement
from corpusparser.sentence import Sentence
from corpusparser.word import Word
import xml.etree.ElementTree as ET   
import re

# Document class represents a complete text document

class Document(CorpusElement):

    # initialise with the provided underlying element
    def __init__(self, element: ET.Element) -> None:
        self.e = element
        self.e.tag = 'document'

    ##############################################################################
    # Object creation methods - overridden from CorpusParser

    # create a document from an underlying element
    def create_from_element(e: ET.Element):
        return Document(e)
    
    # create a document from a text string
    def create_from_xml_string(text: str):
        new_e = ET.fromstring(text)
        return Document.create_from_element(new_e)
    
    # create a document from a file
    def create_from_xml_file(filename: str):
        tree = ET.parse(filename)
        return Document.create_from_element(tree.getroot())
    
    # create a document from new
    def create_new():
        new_e = ET.Element('document')
        return Document(new_e)

    # create a document as a new object in the tree
    def append_new(parent, tag: str):
        new_e = ET.SubElement(parent.get_underlying_element(), tag)
        return Document(new_e)

    ##############################################################################

    # clone an existing document
    def clone_document(self):
        new_elem = self.clone_element()
        return Document.create_from_element(new_elem)

    # create a document from a non-XML, or a non-standard XML file
    def create_from_nonstandard_file(filename:str, format:str):

        if format == 'colmep':

            input_tree = ET.parse(filename)
            d = Document.create_new()

            # traverse the input tree and copy corresponding (but adjusted) elements into our new Document

            for elem in input_tree.getroot().iter():
                # the iterator picks up the document element itself, so skip that
                if elem.tag != 'document':

                    # for each child item, copy the element and append it to the new document root
                    new_elem = ET.SubElement(d.get_underlying_element(), elem.tag, elem.attrib)
                    new_elem.text = elem.text

                    # if there is a tail, create a new <text> element using the tail text
                    if elem.tail != None:
                        if elem.tail != '' and elem.tail != '\n':
                            text_elem = ET.SubElement(d.get_underlying_element(), 'text')
                            text_elem.text = elem.tail

            # at this stage the XML is in an intermediate stage, we now need to convert to our document-word form
            # set up current document, sentence and word
            w = None

            # clone the document and clear the original - it will be easier to copy across than to keep track of iterators
            d_old = d.clone_document()
            d.clear()

            # iterate across the existing document
            for elem in d_old.iter():
                    
                # if this is a text element
                if elem.tag == 'text':

                    # split the text into tokens based on whitespace
                    tokens = elem.text.split()

                    # iterate across each token
                    for token in tokens:
                        # add the token to the document as a w element
                        # NB this will include punctuation
                        w = ET.SubElement(d.get_underlying_element(), 'w')
                        w.text = token

                # if this is a page, comment or footnote tag, copy it into the document
                if elem.tag in ['newpage', 'newfolio', 'comment', 'footnote']:
                    tag = ET.SubElement(d.get_underlying_element(), elem.tag)
                    tag.text = elem.text
                    attribs = elem.attrib.items()
                    tag.attrib.update(attribs)

            return d
        # end of colmep format
                    

    ##############################################################################

    def get_sentences(self) -> list:
        sent_elems = self.get_sentences_as_elements()
        sent_list = []
        for s in sent_elems:
            sent_list.append(Sentence.create_from_element(s))
        return sent_list
    
    def get_words(self) -> list:
        word_elems = self.get_words_as_elements()
        word_list = []
        for w in word_elems:
            word_list.append(Word.create_from_element(w))
        return word_list
    