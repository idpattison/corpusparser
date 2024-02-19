import xml.etree.ElementTree as ET   

# Document class handles everything around importing and exporting documents
class Document(ET.Element):
    def __init__(self) -> None:
        super().__init__('document')

    def import_colmep_format(self, filename: str, name: str, basic=False) -> None:
        # ensure the document is empty
        self.clear()

        # import the file into basic XML format and name it
        self.import_colmep_to_basic(filename)
        self.set('name', name)

        # if required, comvert from basic format to standard
        if not basic:
            self.convert_basic_to_standard()


    def import_colmep_to_basic(self, filename: str) -> None:
        # parse the file into a temporary ElementTree and iterate across it
        tmp_tree = ET.parse(filename)

        for elem in tmp_tree.getroot().iter():

            # the iterator picks up the document element itself, so skip that
            if elem.tag != 'document':

                # for each child item, copy the element and append it to the document root
                new_elem = ET.SubElement(self, elem.tag, elem.attrib)
                new_elem.text = elem.text

                # if there is a tail, create a new <text> element using the tail text
                if elem.tail != None:
                    if elem.tail != '' and elem.tail != '\n':
                        text_elem = ET.SubElement(self, 'text')
                        text_elem.text = elem.tail


    def convert_basic_to_standard(self) -> None:
        # set up current document, sentence and word
        w = None

        # clone the document and clear the original - it will be easier to copy across than to keep track of iterators
        d_old = self.clone_document()
        self.clear()
        self.set('name', d_old.get('name'))

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
                    w = ET.SubElement(self, 'w')
                    w.text = token

            # if this is a page, comment or footnote tag, copy it into the document
            if elem.tag in ['newpage', 'newfolio', 'comment', 'footnote']:
                tag = ET.SubElement(self, elem.tag)
                tag.text = elem.text
                attribs = elem.attrib.items()
                tag.attrib.update(attribs)
    
    # count elements within the document
    def count_elements(element: ET.Element, type: str) -> int:
        return _count_elements(element, type)
    
    # clone a document
    def clone_document(self) -> None:
        return _clone_element(self)

    # clear a document
    def clear_children(self) -> None:
        return _clear_children(self)

    # return a list of all sentences in the document
    def get_sentence_text(self) -> list:
        sents = []
        for s in self.iter('s'):
            sents.append(s.get('text'))
        return sents

    # get a sentence from its index
    def get_sentence_by_index(self, index:int) -> ET.Element:
        return self.findall('s')[index]
    
    # get a word from its index in a sentence
    def get_word_by_index_in_sentence(self, sentence: ET.Element, index:int) -> ET.Element:
        return sentence.findall('w')[index]
    
    # get all sentence elements
    def get_sentence_elements(self) -> list:
        return self.findall('s')







# create a new deep copy of any element in the tree
def _clone_element(element: ET.Element) -> ET.Element:
    # the easiest way is to convert to an XML string then parse back out
    xml = ET.tostring(element, encoding='unicode')
    return ET.fromstring(xml)

# clear all children from the tree
def _clear_children(element: ET.Element) -> None:
    text = element.text
    tail = element.tail
    attribs = element.attrib.items()
    element.clear()
    element.text = text
    element.tail = tail
    element.attrib.update(attribs)

# utility class to count elements - called from Corpus or Document
def _count_elements(element: ET.Element, type: str) -> int:
    count = 0
    for elem in element.iter(type):
        count += 1
    return count