import xml.etree.ElementTree as ET

class CorpusElement():
    def __init__(self, element: ET.Element) -> None:
        self.e = element
    def get_name(self):
        return self.e.get('name')
    def set_name(self, name):
        return self.e.set('name', name)
    def __getitem__(self, index):
        return self.e[index]
    def get_underlying_element(self):
        return self.e
    
class Doc(CorpusElement):
    def __init__(self, element: ET.Element) -> None:
        return super().__init__(element)
    def get_from_element(e: ET.Element):
        return Doc(e)
    def get_from_xml_string(text: str):
        new_e = ET.fromstring(text)
        return Doc.get_from_element(new_e)
    
class Sub(CorpusElement):
    def __init__(self, element: ET.Element) -> None:
        return super().__init__(element)
    def get(e: ET.Element):
        return Sub(e)
    def get_by_index(parent: CorpusElement, index: int):
        ix_e = parent[index]
        return Sub.get(ix_e)
    def create(parent: CorpusElement):
        new_e = ET.SubElement(parent.get_underlying_element(), 'sub')
        return Sub(new_e)
    
d = Doc.get_from_xml_string('<doc name="test"><sub name="test2" /></doc>')
# root = ET.fromstring('<doc name="test"><sub name="test2" /></doc>')
# d = Doc.get_from_element(root)
s = Sub.create(d)
s.set_name("test3")
txt = ET.tostring(d.get_underlying_element())
print(txt)
# n = d.get_name()
# print(n)
# e = d[1]
# s = Sub.get(e)
s = Sub.get_by_index(d, 1)
print(s.get_name())