from src.corpus_element import CorpusElement
from src.word import Word
from collections import deque
import xml.etree.ElementTree as ET   

# NB need to run the following commands in the terminal before running this code
# pip3 install benepar
# python3 -m spacy download en_core_web_md

import benepar, spacy

# global variables
nlp = None
prepared = False

# Sentence class represents a sentence in the text

class Sentence(CorpusElement):

    # initialise with the provided underlying element
    def __init__(self, element: ET.Element) -> None:
        self.e = element
        self.e.tag = 's'

    ##############################################################################
    # Object creation methods - overridden from CorpusParser

    # create a sentence from an underlying element
    def create_from_element(e: ET.Element):
        return Sentence(e)
    
    # create a sentence from a text string
    def create_from_xml_string(text: str):
        new_e = ET.fromstring(text)
        return Sentence.create_from_element(new_e)
    
    # create a sentence from new
    def create_new():
        new_e = ET.Element('s')
        return Sentence(new_e)

    # create a sentence as a new object in the tree
    def append_new(parent, tag: str):
        new_e = ET.SubElement(parent.get_underlying_element(), tag)
        return Sentence(new_e)
    
    # create a sentence from a specific index in a parent
    def create_from_parent_and_index(parent: CorpusElement, index: int):
        sent_e = parent.get_sentence_element_by_index(index)
        return Sentence.create_from_element(sent_e)
    
    ##############################################################################

    def get_words(self) -> list:
        word_elems = self.get_words_as_elements()
        word_list = []
        for w in word_elems:
            word_list.append(Word.create_from_element(w))
        return word_list

    def get_words_as_text(self) -> str:
        return self.get_children_as_text('w')
    
    ##############################################################################
    
    def prepare_parser(self) -> None:
        global nlp
        benepar.download('benepar_en3')
        nlp = spacy.load('en_core_web_md')
        nlp.add_pipe('benepar', config={'model': 'benepar_en3'})

    def parse(self, add_parse_string=False, restructure=False) -> None:
        # first check to see if we have prepared the parser
        global prepared
        if not prepared:
            self.prepare_parser()
            prepared = True

        # get the text of the sentence    
        text = self.get_words_as_text()
        doc = nlp(text)
        sent = list(doc.sents)[0]
        parse = sent._.parse_string

        # save the parse string to the sentence if required
        if add_parse_string:
            self.set_attribute('parse', parse)
        
        # restructure the sentence tree if required
        if restructure:
            self.restructure(parse)

    def restructure(self, parse) -> None:

        # Copy all elements in the sentence to element_list
        # this will include words and other tags such as footnotes
        # implement a a deque, as we will remove elements from the start as we process them
        element_list = deque(self.get_children_as_elements())
        # remove the first element, which is the sentence element
        element_list.popleft()

        # Clear all children from the sentence - we will rebuild in situ
        self.clear_children()

        # Split the parse string into list items - call this parse_list
        # This will contain three types of parse instruction
        # (X followed immediately by another (X - a phrase
        # (X followed immediately by an X) - a pos type
        # X) - a word - the number of closing parentheses is significant
        parse_list = parse.split(' ')

        # Create a stack for the phrase elements - call this phrase_stack
        # initialise with the sentence element, which is our top-level phrase
        phrase_stack = [self.e]

        # variable to hold the current pos type
        pos_type = None

        # Iterate through parse_list
        for parse_item in range(len(parse_list)):

            # For each item
            item = parse_list[parse_item]
            # If it’s a phrase
            if item.startswith('(') and parse_list[parse_item + 1].startswith('('):
                # Create a phrase element - mark its type
                # Add it to the current phrase element
                new_phrase = ET.SubElement(phrase_stack[-1], 'phr')
                new_phrase.set('type', item[1:])
                # Add it to phrase_stack (NB the most recent item in this stack is the current phrase)
                phrase_stack.append(new_phrase)
                print('item ', item)
                print('new phrase added to ', phrase_stack[-1].tag)
                print('\n')

            # If it’s a pos type
            elif item.startswith('('):
                # Record it as the current pos type
                pos_type = item[1:]
                print('item ', item)
                print('pos type set to ', pos_type)
                print('\n')

            # If it’s a word
            elif item.endswith(')'):
                # Get the next word from element_list (we should be at a word, not a non-word)
                word = element_list.popleft()
                # Add it to the current phrase element
                phrase_stack[-1].append(word)
                # Set the pos type to the current pos type
                word.set('pos', pos_type)
                # Count the parentheses at the end - this will be used later
                count = item.count(')') - 1
                # If the next item is a non-word, also add that to the current phrase
                # Repeat until we are at a word again
                print('item ', item)
                print('word added to ', phrase_stack[-1].tag)
                while len(element_list) > 0 and element_list[0].tag != 'w':
                    nonword = element_list.popleft()
                    phrase_stack[-1].append(nonword)
                    print('non-word ', nonword.tag, ' added to ', phrase_stack[-1].tag)
                # Now count the parentheses - subtract one - pop that many phrases off phrase_stack
                for x in range(count):
                    phrase_stack.pop()
                print('popped from phrase stack: ', count)
                print('phrase stack length: ', len(phrase_stack))
                print('\n')

        #TODO Optionally add a POS string without parse data
        #TODO Don’t forget document ID and sentence number

