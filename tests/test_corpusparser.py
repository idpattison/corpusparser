import unittest

from src.document import Document
from src.sentence import Sentence
from src.word import Word

import xml.etree.ElementTree as ET

class ImportColmepTestCase(unittest.TestCase):

    # import the xml.file into a Document
    def setUp(self) -> None:
        filename = 'tests/data/input.xml'
        docname = 'Test document'
        format = 'colmep'
        self.d = Document.create_from_nonstandard_file(filename, format)
        self.d.set_name(docname)
        # self.d.import_colmep_format(filename, docname)
        return super().setUp()

    # check that the root is a document with the correct name
    def test_imported_file_is_a_document(self):
        # check for document element
        self.assertEqual(self.d.get_tag(), 'document') 
        # check for document name
        self.assertEqual(self.d.get_name(), 'Test document')

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
        format = 'colmep'
        self.d = Document.create_from_nonstandard_file(filename, format)
        self.d.set_name(docname)
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
        self.assertEqual(self.d.get_name(), 'Test document')
        
    # check that the clone document function works
    def test_clone_document(self):
        d_new = self.d.clone_document()
        # check there are the same number of child elements
        self.assertEqual(Document.count_elements(d_new, 'comment'), 6)
        # check the document name has been cloned
        self.assertEqual(d_new.get_name(), 'Test document')
        
    
class SentencesAndWordsTestCase(unittest.TestCase):    

    # import the xml file into a Document and process sentences
    def setUp(self) -> None:
        filename = 'tests/data/input.xml'
        format = 'colmep'
        self.d = Document.create_from_nonstandard_file(filename, format)
        self.d.transform_tokenise_sentences()
        self.d.transform_add_convenience_text_to_sentences()
        return super().setUp()
    
    # check that we can get all sentences from the text
    def test_get_sentence_text(self):
        sents = self.d.get_sentences_as_text_list()
        # check this is the right size
        self.assertEqual(len(sents), 39)
        # check a given sentence
        self.assertEqual('As the philosopher', sents[2][:18])

    # check that we can get the sentence elements
    def test_get_sentence_element(self):
        sents = self.d.get_sentences_as_elements()
        # check this is the right size
        self.assertEqual(len(sents), 39)

    # check we can get Sentence objects
    def test_get_sentences(self):
        sents = self.d.get_sentences()
        # check that the elements are Sentences
        s = sents[2]
        self.assertIsInstance(s, Sentence)
        # check a given sentence
        t = s.get_attribute('conv-text')
        self.assertEqual('As the philosopher', t[:18])
        
    # check that we can retrieve a given sentence and word
    def test_get_specific_word(self):
        # the 3rd word of the 3rd sentence should be 'philosopher'
        word = Word.create_from_sentence_and_word_index(self.d, 2, 2)
        # sent = self.d.get_sentence_by_index(2)
        # word = self.d.get_word_by_index_in_sentence(sent, 2)
        self.assertEqual(word.get_text(), 'philosopher')

    # check sentence and word lengths
    def test_sentence_lengths(self):
        words = self.d.count_words()
        self.assertEqual(words, 1772)
        longest = self.d.longest_sentence_length()
        self.assertEqual(longest, 124)



class SpellingCorrectionTestCase(unittest.TestCase):    

    # import the xml file into a Document and process sentences
    def setUp(self) -> None:
        filename = 'tests/data/input.xml'
        format = 'colmep'
        self.d = Document.create_from_nonstandard_file(filename, format)
        self.d.transform_tokenise_sentences()
        return super().setUp()
    
    # check that spelling updates are applied correctly
    def test_remove_asterisks(self):
        self.d.transform_remove_asterisks()
        # check the words have been correctly updated and the old orthography stored
        # word 15 in sentence 3 is *that*
        word = self.d.get_word_element_by_sentence_and_word_index(2, 14)
        self.assertEqual(word.text, 'that')
        self.assertEqual(word.get('ortho'), '*that*')
        # check another word
        # word 2 in sentence 5 is vpo*n*
        word = self.d.get_word_element_by_sentence_and_word_index(4, 1)
        self.assertEqual(word.text, 'vpon')
        self.assertEqual(word.get('ortho'), 'vpo*n*')



class SentenceParseTestCase(unittest.TestCase):    

    # import the xml file into a Document and process sentences
    def setUp(self) -> None:
        filename = 'tests/data/input.xml'
        format = 'colmep'
        self.d = Document.create_from_nonstandard_file(filename, format)
        self.d.transform_tokenise_sentences()
        self.d.transform_parse(add_parse_string=True, restructure=True)
        return super().setUp()
    
    # check that parsing has been applied
    def test_remove_asterisks(self):
        # check that the parse string has been added to the sentence
        sents = self.d.get_sentences()
        s = sents[0]
        parse = s.get_attribute('parse')
        self.assertEqual('(S (: ¶) (NP (NP (DT The)', parse[:25])
        # check that the sentences have been restructured
        se = sents[1].get_underlying_element()
        e = se[0]  # should be a phrase
        self.assertEqual(e.tag, 'phr')



if __name__ == '__main__':
    unittest.main()
