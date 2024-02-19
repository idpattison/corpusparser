import xml.etree.ElementTree as ET   

class Corpus(ET.Element):
    # count elements within the corpus
    def count_elements(element: ET.Element, type: str) -> int:
        return _count_elements(element, type)