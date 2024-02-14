import unittest

from src.document import Document, Corpus
import xml.etree.ElementTree as ET

class ImportColmepBasicTestCase(unittest.TestCase):

    # import the xml.file into a Document
    def setUp(self) -> None:
        filename = 'tests/data/input.xml'
        docname = 'Test document'
        self.d = Document()
        self.d.import_colmep_format(filename, docname, basic=True)
        # create a list of all the child elements
        self.d_list = list(self.d)
        return super().setUp()

    # check that the root is a document with the correct name
    def test_basic_imported_file_is_a_document(self):
        # check for document element
        self.assertEqual(self.d.tag, 'document') 
        # check for document name
        self.assertEqual(self.d.get('name'), 'Test document') 

    # check that xml text matches the sample
    # def test_basic_imported_file_xml_output(self):
    #     # export xml
    #     xml = ET.tostring(self.d, encoding='unicode') 
    #     # import sample and compare
    #     file = open('tests/data/stage1.xml')
    #     sample = file.read()
    #     self.assertEqual(xml, sample)


class ImportColmepStandardTestCase(unittest.TestCase):

    # import the xml.file into a Document
    def setUp(self) -> None:
        filename = 'tests/data/input.xml'
        docname = 'Test document'
        self.d = Document()
        self.d.import_colmep_format(filename, docname)
        return super().setUp()

    # check that the root is a document with the correct name
    def test_imported_file_is_a_document(self):
        # check for document element
        self.assertEqual(self.d.tag, 'document') 
        # check for document name
        self.assertEqual(self.d.get('name'), 'Test document')

    # check that the first newpage element has pageno = 1
    def test_imported_file_newpage(self):
        # check for newpage element
        for elem in self.d.iter('newpage'):
            self.assertEqual(elem.get('pageno'), '1')
            break

    # check that the first comment element has the correct comtext
    def test_imported_file_comment(self):
        # check for comment element
        for elem in self.d.iter('comment'):
            self.assertIn('First page with title', elem.get('comtext')) 
            break

    # check that the first word element is correct
    def test_imported_file_text(self):
        # check for first text element
        for elem in self.d.iter('w'):
            self.assertEquals(elem.text, '¶') 
            break


class UtilityFunctionsTestCase(unittest.TestCase):

    # import the xml file into a Document
    def setUp(self) -> None:
        filename = 'tests/data/input.xml'
        docname = 'Test document'
        self.d = Document()
        self.d.import_colmep_format(filename, docname)
        return super().setUp()

    # check that the element counting function works
    def test_count_elements(self):
        self.assertEqual(Document.count_elements(self.d, 'comment'), 6)

    # check that the clear document children function works
    def test_clear_children(self):
        self.d.clear_children()
        # check there are no child elements
        self.assertEqual(Document.count_elements(self.d, 'comment'), 0)
        # check the document name is still in place
        self.assertEqual(self.d.get('name'), 'Test document')
        
    # check that the clone document function works
    def test_clone_document(self):
        d_new = self.d.clone_document()
        # check there are the same number of child elements
        self.assertEqual(Document.count_elements(d_new, 'comment'), 6)
        # check the document name has been cloned
        self.assertEqual(d_new.get('name'), 'Test document')
        


if __name__ == '__main__':
    unittest.main()
