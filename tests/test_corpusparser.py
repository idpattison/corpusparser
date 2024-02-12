import unittest

import src.corpusparser as CP
import xml.etree.ElementTree as ET

class ImportDataTestCase(unittest.TestCase):

    # dummy test - designed to break
    def test_dummy(self):
        self.assertEquals(0, 1)

    # import the input.xml file into a Document and check the root is a document
    def test_imported_file_is_a_document(self):
        filename = 'data/input.xml'
        d = CP.Document(filename, 'Dummy name')
        self.assertEqual(d.getroot().tag, 'document') 

if __name__ == '__main__':
    unittest.main()
