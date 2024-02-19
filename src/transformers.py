import xml.etree.ElementTree as ET
from src.document import Document
import re

# A set of classes which transform the corpus tree from one state to another
class Transformers():

    def transform_tokenise_sentences(d: Document, tokenisation_model='period') -> None:
        # split the words into sentences
        # start with a set of <w> elements which are children of the <document>
        # create <s> elements to hold the <w> elements in each sentence

        # create an ordered list of word elements - NB this can be punctuation also
        word_elem_list = list(d.iter('w'))

        # iterate through the list and call the tokenisation model for each word
        # if the model predicts this is the last word of a sentence, add a 'sent-break' attribute to flag this
        for i in range(0, len(word_elem_list)):

            # choose the tokenisation model
            if tokenisation_model == 'period':
                if _period_tokenisation_model(word_elem_list, i):
                    word_elem_list[i].set('sent-break', '1')

            # NB no other tokenisation models at present

        # the last word will always be a sentence break
        word_elem_list[-1].set('sent-break', '1')

        # clone the document and clear the existing children
        old_doc = d.clone_document()
        d.clear_children()

        # iterate through all child elements of the original document
        s = None
        for elem in old_doc.iter():

            # the iterator picks up the document itself - ignore this
            if elem.tag != 'document':

                # if this element is a word
                if elem.tag == 'w':
                    # if there is no sentence, create one, append it to the document
                    if s == None:
                        s = ET.SubElement(d, 's')

                    # add the word to the sentence
                    # TODO - do we need to clone this?
                    s.append(elem)

                    # if this word is sentence breaking
                    if elem.get('sent-break') == '1':
                        # set the sentence back to None to signify it has ended and we need a new one
                        s = None

                # if not a word
                else:
                    # copy the element to the sentence is we have one, or the document if not
                    if s == None:
                        d.append(elem)
                    else:
                        s.append(elem) 

    def transform_add_text_to_sentences(d: Document) -> None:
        # iterate through the sentences, for each one
        # concatenate the words and add to a text attribute in the sentence
        for sentence in d.iter('s'):
            words = []
            for w in sentence.iter('w'):
                if w.text != None:
                    words.append(w.text)
            if len(words) > 0:
                text = ' '.join(words)
                sentence.set('text', text)

    def transform_remove_asterisks(d: Document) -> None:
        _update_spellings(d, '\*', '')


        

# Utility functions

def _period_tokenisation_model(word_list, index: int) -> bool:
    if word_list[index].text == '.':
        return True
    return False

def _update_spellings(d: Document, match: str, replace: str) -> None:
    # for each word, check if it matches the regex pattern
    # if so, make corrections, and add the original orthography to the word as an attribute
    pattern = re.compile(match)
    for w in d.iter('w'):
        if pattern.match(w.text):
            w.set('ortho', w.text)
            w.text = pattern.sub(replace, w.text)

