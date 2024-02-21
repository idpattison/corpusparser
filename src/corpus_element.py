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
    def xml_string(self) -> str:
        return ET.tostring(self.e)
    #TODO - write to file


