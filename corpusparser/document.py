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
    
    # count elements within the document
    # def count_elements(element: ET.Element, type: str) -> int:
    #     return _count_elements(element, type)
    
    # # clone a document
    # def clone_document(self) -> None:
    #     return _clone_element(self.get_underlying_element())

    # clear a document
    # def clear_children(self) -> None:
    #     return _clear_children(self)

    # return a list of all sentences in the document
    # def get_sentence_text(self) -> list:
    #     sents = []
    #     for s in self.iter('s'):
    #         sents.append(s.text)
    #     return sents

    # get a sentence from its index
    # def get_sentence_by_index(self, index:int) -> ET.Element:
    #     return self.findall('s')[index]
    
    # # get a word from its index in a sentence
    # def get_word_by_index_in_sentence(self, sentence: ET.Element, index:int) -> ET.Element:
    #     return sentence.findall('w')[index]
    
    # # get a word from its sentence & word index
    # def get_word_by_index(self, sentence_index: int, word_index:int) -> ET.Element:
    #     s = self.get_sentence_by_index(sentence_index)
    #     return self.get_word_by_index_in_sentence(s, word_index)
    
    # # get all sentence elements
    # def get_sentence_elements(self) -> list:
    #     return self.findall('s')

    # # get all word elements
    # def get_word_elements(self) -> list:
    #     return self.findall('w')

    # # get count of sentences
    # def get_sentence_count(self) -> int:
    #     return len(self.get_sentence_elements())
    
    # # get count of words
    # def get_word_count(self) -> int:
    #     return len(self.get_word_elements())
    
    # get count of words in a given sentence
    # def get_sentence_length(sentence: ET.Element) -> int:
    #     return len(sentence.findall('w'))
    
    # # get sentence length - longest, shortest, average
    # def get_longest_sentence(self) -> int:
    #     return max(self._get_sentence_lengths())
    # def get_shortest_sentence(self) -> int:
    #     return min(self._get_sentence_lengths())
    # def get_average_sentence_length(self) -> int:
    #     lengths = self._get_sentence_lengths()
    #     return round(sum(lengths) / len(lengths))
    # def _get_sentence_lengths(self) -> list:
    #     sent_lengths = []
    #     for s in self.findall('s'):
    #         sent_lengths.append(len(s.findall('w')))
    #     return sent_lengths


# TRANSFORM FUNCTIONS

    # def transform_tokenise_sentences(self, tokenisation_model='period') -> None:
    #     # split the words into sentences
    #     # start with a set of <w> elements which are children of the <document>
    #     # create <s> elements to hold the <w> elements in each sentence

    #     # create an ordered list of word elements - NB this can be punctuation also
    #     word_elem_list = list(self.e.iter('w'))

    #     # iterate through the list and call the tokenisation model for each word
    #     # if the model predicts this is the last word of a sentence, add a 'sent-break' attribute to flag this
    #     for i in range(0, len(word_elem_list)):

    #         # choose the tokenisation model
    #         if tokenisation_model == 'period':
    #             if _period_tokenisation_model(word_elem_list, i):
    #                 word_elem_list[i].set('sent-break', '1')

    #         # NB no other tokenisation models at present

    #     # the last word will always be a sentence break
    #     word_elem_list[-1].set('sent-break', '1')

    #     # clone the document and clear the existing children
    #     old_doc = self.clone_document()
    #     self.clear_children()

    #     # iterate through all child elements of the original document
    #     s = None
    #     for elem in old_doc.iter():

    #         # the iterator picks up the document itself - ignore this
    #         if elem.tag != 'document':

    #             # if this element is a word
    #             if elem.tag == 'w':
    #                 # if there is no sentence, create one, append it to the document
    #                 if s == None:
    #                     s = ET.SubElement(self, 's')

    #                 # add the word to the sentence
    #                 # TODO - do we need to clone this?
    #                 s.append(elem)

    #                 # if this word is sentence breaking
    #                 if elem.get('sent-break') == '1':
    #                     # set the sentence back to None to signify it has ended and we need a new one
    #                     s = None

    #             # if not a word
    #             else:
    #                 # copy the element to the sentence is we have one, or the document if not
    #                 if s == None:
    #                     self.append(elem)
    #                 else:
    #                     s.append(elem) 

    # def transform_add_text_to_sentences(self) -> None:
    #     # iterate through the sentences, for each one
    #     # concatenate the words and add to a text attribute in the sentence
    #     for sentence in self.iter('s'):
    #         words = []
    #         for w in sentence.iter('w'):
    #             if w.text != None:
    #                 words.append(w.text)
    #         if len(words) > 0:
    #             text = ' '.join(words)
    #             sentence.text = text

    # def transform_remove_asterisks(self) -> None:
    #     _update_spellings(self, '\*', '')


# UTILITY FUNCTIONS

# create a new deep copy of any element in the tree
# def _clone_element(element: ET.Element) -> ET.Element:
#     # the easiest way is to convert to an XML string then parse back out
#     xml = ET.tostring(element, encoding='unicode')
#     return ET.fromstring(xml)

# clear all children from the tree
# def _clear_children(element: ET.Element) -> None:
#     text = element.text
#     tail = element.tail
#     attribs = element.attrib.items()
#     element.clear()
#     element.text = text
#     element.tail = tail
#     element.attrib.update(attribs)

# utility class to count elements - called from Corpus or Document
# def _count_elements(element: ET.Element, type: str) -> int:
#     count = 0
#     for elem in element.iter(type):
#         count += 1
#     return count

# def _period_tokenisation_model(word_list, index: int) -> bool:
#     if word_list[index].text == '.':
#         return True
#     return False

# def _update_spellings(d: Document, match: str, replace: str) -> None:
#     # for each word, check if it matches the regex pattern
#     # if so, make corrections, and add the original orthography to the word as an attribute
#     pattern = re.compile(match)
#     for w in d.iter('w'):
#         if pattern.match(w.text):
#             w.set('ortho', w.text)
#             w.text = pattern.sub(replace, w.text)