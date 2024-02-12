import xml.etree.ElementTree as ET

# create some classes to help with type-checking
class Corpus(ET.Element):
    pass

class Document(ET.Element):
    def __init__(self, filename: str, name: str) -> None:
        super().__init__()
        self.attrib.update('name', name)
        x = filename

    def get_name(self) -> str:
        return self.attribs.get('name')

class Sentence(ET.Element):
    pass

class Word(ET.Element):
    pass



