import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from corpusparser.corpus_element import CorpusElement
from corpusparser.corpus import Corpus
from corpusparser.document import Document
from corpusparser.sentence import Sentence
from corpusparser.word import Word