import unittest

from src.corpusparser import Document
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

    # # check that the first child element is a newpage with pageno = 1
    # def test_imported_file_newpage(self):
    #     # check that there are some elements
    #     self.assertFalse(not self.d_list)
    #     # check for newpage element
    #     self.assertEqual(self.d_list[0].tag, 'newpage') 
    #     # check for pageno
    #     self.assertEqual(self.d_list[0].get('pageno'), '1') 

    # # check that the next child element is a comment with the correct comtext
    # def test_imported_file_comment(self):
    #     # check for comment element
    #     self.assertEqual(self.d_list[1].tag, 'comment') 
    #     # check for comment text
    #     self.assertIn('First page with title', self.d_list[1].get('comtext')) 

    # # check that the next child element is a text element with the correct text
    # def test_imported_file_text(self):
    #     # check for first text element
    #     self.assertEqual(self.d_list[2].tag, 'text') 
    #     # check for text 
    #     self.assertIn('¶ The right plesaunt and goodly historie', self.d_list[2].text) 

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



if __name__ == '__main__':
    unittest.main()
