# Represents any element in the XML tree
# the actual element is an xml.etree.ElementTree.Element
# this class wraps some additional functions relevant to corpora
# and serves as the parent class for more specialised classes


import xml.etree.ElementTree as ET

class CorpusElement():

    # the underlying XML tree element
    e = None

    # initialise with the provided underlying element
    def __init__(self, element: ET.Element) -> None:
        self.e = element

    # this makes the class (and any subclasses) subscriptable
    # e.g. if cp is a CorpusParser object, element = cp[0] returns the 
    # first sub-element
    # NB this will return the underlying element, not the CorpusParser object
    def __getitem__(self, index):
        return self.e[index]

    # retrieve the underlying element if this is needed for more detailed analysis
    def get_underlying_element(self) -> ET.Element:
        return self.e
    
    ##############################################################################
    # Object creation methods - subclasses should override these
    ##############################################################################

    # create an object from an underlying element
    def create_from_element(e: ET.Element):
        return CorpusElement(e)
    
    # create an object from a text string
    def create_from_xml_string(text: str):
        new_e = ET.fromstring(text)
        return CorpusElement.create_from_element(new_e)
    
    # create an object from a file
    # NB this expects a standard corpusparser XML format
    # other formats may need to be manipulated by subclasses
    def create_from_xml_file(filename: str):
        tree = ET.parse(filename)
        return CorpusElement.create_from_element(tree.getroot())

    # create an object as a new object in the tree
    def append_new(parent, tag: str):
        new_e = ET.SubElement(parent.get_underlying_element(), tag)
        return CorpusElement(new_e)
    
    # End of object creation methods
    ##############################################################################
    
    
    ##############################################################################
    # Operations
    ##############################################################################

    # count sub-elements within this element
    def count_elements(self, tag=None) -> int:
        return len(list(self.e.iter(tag)))
    
    # create a new deep copy of any element in the tree
    def clone_element(self) -> ET.Element:
        # the easiest way is to convert to an XML string then parse back out
        xml = ET.tostring(self.e, encoding='unicode')
        return ET.fromstring(xml)
    
    # clear all sub-elements from the element
    def clear_children(self) -> None:
        text = self.e.text
        tail = self.e.tail
        attribs = self.e.attrib.items()
        self.e.clear()
        self.e.text = text
        self.e.tail = tail
        self.e.attrib.update(attribs)



    ##############################################################################
    # Sub-element retrieval functions
    ##############################################################################

    # return the text of all sub-elements of a given type contained in this element as a list of strings
    def get_children_as_text(self, tag: str) -> list:
        children = []
        for c in self.e.iter(tag):
            children.append(c.text)
        return children

    # return all sub-elements of a given type contained in this element as a list
    def get_children_as_elements(self, tag: str) -> list:
        children = []
        for c in self.e.iter(tag):
            children.append(c)
        return children

    # return all sentences as a list of strings or elements
    def get_sentences_as_text(self) -> list:
        return self.get_children_as_text('s')
    def get_sentences_as_elements(self) -> list:
        return self.get_children_as_elements('s')

    # return all word as a list of strings or elements
    def get_words_as_text(self) -> list:
        return self.get_children_as_text('w')
    def get_words_as_elements(self) -> list:
        return self.get_children_as_elements('w')

    # return all documents as a list of elements
    def get_documents_as_elements(self) -> list:
        return self.get_children_as_elements('document')
    
    # return a specific sub-element by index
    # if we need these to be recursive use iter() instead of findall()
    def get_child_by_index(self, tag: str, index: int, recursive=True) -> ET.Element:
        if recursive:
            return list(self.iter(tag))[index]
        return self.findall(tag)[index]
    
    # word- and sentence-specific functions
    def get_word_element_by_index(self, index: int) -> ET.Element:
        return self.get_child_by_index('w', index, recursive=True)
    def get_sentence_element_by_index(self, index: int) -> ET.Element:
        return self.get_child_by_index('s', index, recursive=True)
    def get_word_element_by_sentence_and_word_index(self, sentence_index: int, word_index: int) -> ET.Element:
        sent_e = self.get_sentence_element_by_index(sentence_index)
        return list(sent_e.iter('w'))[word_index]



    ##############################################################################
    # Count methods
    ##############################################################################

    # get count of specific element types
    def get_element_count(self, tag: str, recursive=True) -> int:
        if recursive:
            return len(list(self.iter(tag)))
        return len(self.findall(tag))
    
    # specific element types
    def get_sentence_count(self) -> int:
        return self.get_element_count('s')
    def get_word_count(self) -> int:
        return self.get_element_count('w')

    # get sentence length - longest, shortest, average
    def get_sentence_lengths(self) -> list:
        sent_lengths = []
        for s in self.get_sentences_as_elements():
            sent_lengths.append(len(list(s.iter('w'))))
        return sent_lengths
    def get_longest_sentence(self) -> int:
        return max(self.get_sentence_lengths())
    def get_shortest_sentence(self) -> int:
        return min(self.get_sentence_lengths())
    def get_average_sentence_length(self) -> int:
        lengths = self.get_sentence_lengths()
        return round(sum(lengths) / len(lengths))
    
    # get count of words in a given sentence
    # def _get_sentence_length(sentence: ET.Element) -> int:
    #     return len(sentence.iter('w'))





    ##############################################################################
    # Helper methods
    ##############################################################################

    # helper methods to retrieve and update data from the underlying element
    def get_tag(self) -> str:
        return self.e.tag
    def set_tag(self, tag) -> None:
        self.e.tag = tag

    def get_text(self) -> str:
        return self.e.text
    def set_text(self, text) -> None:
        self.e.text = text

    def get_tail(self) -> str:
        return self.e.tail
    def set_tail(self, tail) -> None:
        self.e.tail = tail

    # helper methods to retrieve and update data from the underlying element's attributes
    def get_name(self) -> str:
        return self.e.get('name')
    def set_name(self, name) -> None:
        self.e.set('name', name)
    
    def get_attribute(self, key) -> str:
        return self.e.get(key)
    def set_attribute(self, key, value) -> None:
        self.e.set(key, value)
    def delete_attribute(self, key) -> None:
        self.e.attrib.pop(key)
    def clear_attributes(self) -> None:
        self.e.attrib.clear()
    
    # helper methods to retrieve sub-elements from the underlying element
    # NB findall() only finds direct children
    # iter() is recursive
    def findall(self, tag: str) -> list:
        return self.e.findall(tag)
    def iter(self, tag=None):
        return self.e.iter(tag)
    
    # helper methods to alter the structure of the underlying element
    def clear(self) -> None:
        self.e.clear()
    def append(self, subelement: ET.Element) -> None:
        self.e.append(subelement)
    def insert(self, index: int, subelement: ET.Element) -> None:
        self.e.insert(index, subelement)
    def remove(self, subelement: ET.Element) -> None:
        self.e.remove(subelement)

    # helper methods to output the tree
    def to_xml_string(self, indent=0, encoding='unicode') -> str:
        if indent > 0:
            space = ' ' * indent
            ET.indent(self.e, space)
        return ET.tostring(self.e, encoding)
    #TODO - write to file



    ##############################################################################
    # Transform functions
    ##############################################################################

    def transform_tokenise_sentences(self, tokenisation_model='period') -> None:
        # split the words into sentences
        # start with a set of <w> elements which are children of the <document>
        # create <s> elements to hold the <w> elements in each sentence

        # create an ordered list of word elements - NB this can be punctuation also
        word_elem_list = list(self.e.iter('w'))

        # iterate through the list and call the tokenisation model for each word
        # if the model predicts this is the last word of a sentence, add a 'sent-break' attribute to flag this
        for i in range(0, len(word_elem_list)):

            # choose the tokenisation model
            if tokenisation_model == 'period':
                if _period_tokenisation_model(word_elem_list, i):
                    word_elem_list[i].set('sent-break', '1')

            # NB no other tokenisation models at present

        # the last word will always be a sentence break
        word_elem_list[-1].set('sent-break', '1')

        # clone the document and clear the existing children
        old_doc = self.clone_document()
        self.clear_children()

        # iterate through all child elements of the original document
        s = None
        for elem in old_doc.e.iter():

            # the iterator picks up the document itself - ignore this
            if elem.tag != 'document':

                # if this element is a word
                if elem.tag == 'w':
                    # if there is no sentence, create one, append it to the document
                    if s == None:
                        s = ET.SubElement(self.e, 's')

                    # add the word to the sentence
                    # TODO - do we need to clone this?
                    s.append(elem)

                    # if this word is sentence breaking
                    if elem.get('sent-break') == '1':
                        # set the sentence back to None to signify it has ended and we need a new one
                        s = None

                # if not a word
                else:
                    # copy the element to the sentence is we have one, or the document if not
                    if s == None:
                        self.append(elem)
                    else:
                        s.append(elem) 

    def transform_add_text_to_sentences(self) -> None:
        # iterate through the sentences, for each one
        # concatenate the words and add to a text attribute in the sentence
        for sentence in self.e.iter('s'):
            words = []
            for w in sentence.iter('w'):
                if w.text != None:
                    words.append(w.text)
            if len(words) > 0:
                text = ' '.join(words)
                sentence.text = text

    # def transform_remove_asterisks(self) -> None:
    #     _update_spellings(self, '\*', '')

# END OF CLASS
##############################################################################



##############################################################################
# Models
##############################################################################

def _period_tokenisation_model(word_list, index: int) -> bool:
    if word_list[index].text == '.':
        return True
    return False



##############################################################################
# Utilities
##############################################################################

    