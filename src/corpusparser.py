import xml.etree.ElementTree as ET

# create some classes to help with type-checking
class Corpus(ET.Element):
    pass

# Document class handles everything aroun importing and exporting documents
class Document(ET.Element):
    def __init__(self) -> None:
        super().__init__('document')

    def import_colmep_format(self, filename: str, name: str) -> None:

        # ensure the document is empty
        self.clear()

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


class Sentence(ET.Element):
    pass

class Word(ET.Element):
    pass



