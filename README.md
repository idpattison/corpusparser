# corpusparser
Python library for importing and using corpus data in linguistic research

## Basic usage

### Installation

```bash
pip install corpusparser
```

### Usage

```python
import corpusparser
doc = corpusparser.Document.create_from_xml_file("myfile.xml")
print(doc.count_words())
```

## Overview

All documents are stored in a standard format which has documents (`<document>`) containing sentences (`<s>`), which in turn contain words (`<w>`), for example:

```xml
<document name="My Historical Text">
  <newpage pageno="1" />
  <comment comtext="First page with title" />
  <s n="1" orig-text="Once vpon a time">
    <w>Once</w>
    <w orth="upon">vpon</w>
    <w>a</w>
    <w>time</w>
  </s>
</document>
```

Four basic operations are allowed on this core structure:

1. Import data from an external source, save it to file, and export to other corpus tools
2. Query the structure for attributes such as number of words
3. Find and edit specific elements in the structure
4. Transform the entire structure to better suit your research needs

## Importing documents

Data can be imported from *standard* format XML files (*i.e.* files previously exported from *corpusparser*. This allows multiple versions of a document to be stored and managed).

Data can also be imported from *non-standard* format files. At present, the only supported non-standard format is CoLMEP format (*Corpus of Late Middle English Prose*). Other formats will be supported in due course. Please feel free to contact the author to discuss.

### Import from a standard format file

Specify the filename and create a new `Document` object

```python
filename = "myfile.xml"
doc = corpusparser.Document.create_from_xml_file(filename)
```

### Import from a non-standard format file

Specify the filename and format and create a new `Document` object

```python
filename = "myfile.xml"
format = "colmep"
doc = corpusparser.Document.create_from_nonstandard_file(filename, format)
```

When creating a new document in this way, it is useful to add key infomration such as the document name and identifier. The identifier can be added to any output which may be useful when subsequently imported to corpus tools such as Sketch Engine.

```python
doc.set_name("My Text Document")
doc.set_id("MYTEXT")
```

### Saving a file

As you apply corrections, edits and transforms to a document, you can save copies of your work to file, so that you can pick up again later, or try other transforms and revert to a saved version if it goes wrong.

```python
filename = "current_work_v2.xml"
doc.to_xml_file(filename, indent=2)
```

The indent applies to the XML and makes it more human readable.

### Exporting in other formats

Sometimes you will need to export data in different formats, for example Sketch Engine will accept plain text sentences with no XML. YOu can query the document using the various functions and write these to file.

To export a document's sentences in plain text, retrieve the sentences as a `List` and write them to file.

```python
sents = d.get_sentences_as_text_list()
filename = "sentences.txt"
try:
    with open(filename, 'w') as f:
        for s in sents:
            f.write(s)
except IOError:
    print("IOError: Could not write to file " + filename)
```

## Querying a document

You can ask for all sorts of information about a document, such as the number of words or sentences, or the frequency of certian words. You can also get a simple concordance output.

### Quick info

To get a quick readout on the basic information about a document, such as sentence and word count, sentence length, most common words with and without punctuation, and the XML tags used:

```python
doc.print_info()
```

### Counting words and sentences

Get the number of words and senetcnes in a document:

```python
doc.count_words()
doc.count_sentences()
```

Check the length of sentences - longest, shortes and average. This can be useful when trying to understand if the document has non-standard punctuation.

```python
doc.longest_sentence_length()
doc.shortest_sentence_length()
doc.average_sentence_length()
```

### Word frequency

To see a list of the 20 most frequent words in a text:

```python
doc.word_frequency().most_common(20)
```

If you have applied any spelling corrections, this will check the original orthography. To check the corrected text instead, use:

```python
doc.word_frequency(correctedText=True)
```

You can also check for the frequency of words which begin with a specific letter, which contain a certain piece of text, or which contain punctuation (or not). This one in particular can help you to understand non-standard punctuation such as asterisks (for nasal consonants) and obliques (for pauses).

```python
doc.word_frequency_starts_with("A")
doc.word_frequency_contains("ing")
doc.word_frequency_contains_punctuation()
doc.word_frequency_no_punctuation()
```

As before, `correctedText=True` can be applied to any of these. Finally, if you need precise control over items in a frequency ditribution, you can apply a *regex* pattern:

```python
pattern = "[Aa][Dd].*"
doc.word_frequency(pattern)
```

### XML tags

For non-standard document input, most tags such as `<comment>` and `<footnote>` are simply passed through without processing. YOu can check which XML tags are present in a dcoument:

```python
doc.get_xml_tags()
```

### Concordance

It is possible to export textual data for import to a corpus manager such as Sketch Engine, however sometimes you need something simpler. 

```python
conc = doc.concordance("thou", correctedText=False, separator="|", context_length=15)
```

This will return a list of concordance contexts, with the left context, KWIC and right context separated by vertical bars. The default separator, if you don't specify one, is a tab character, and the default context length is 25.

You can also specify multiple keywords, for example this will find all examples of *which*, *whiche* and *whyche* and output a tab-separated variable file, suitable for importing into a spreadsheet:

```python
conc = d.concordance_in(['which', 'whiche', 'whyche'])
filename = "which.tsv"
try:
    with open(filename, 'w') as f:
        for c in conc:
            f.write(c)
except IOError:
    print("IOError: Could not write to file " + filename)
```

## Surgical editing

You can retrieve a specific sentence or word and correct it, or otherwise manipulate it to add new information. For example, to retrieve a specific sentence by its index:

```python
sent = corpusparser.Sentence.create_from_parent_and_index(doc, 5)
sent.get_words_as_text()
```

NB this will retrieve the 6th sentence in the document. Bear in mind that in Python, indices are *0-based*.

To retrieve the 4th word in the 8th sentence and add an attribute to (for example) show this is a raising verb:

```python
word = corpusparser.Word.create_from_sentence_and_word_index(doc, 7, 3)
word.set_attribute("verb-type", "raising")
```

This would result in an XML structure like this: 

```xml
<w verb-type="raising">presume</w>
```

You can retrieve and update an element's text or any of its attributes. You can also create a new attribute, query if an element has a specific attribute, and delete existing ones.

```python
word.get_text()
word.set_text("new text")
word.get_attribute("attr-name")
word.set_attribute("attr-name", "value")  # updates or creates
word.has_attribute("attr-name")  # returns True or False
word.delete_attribute("attr-name")
```

## Transform the structure

As well as surgically editing specific parts of the document structure, you can apply *transformations* to the entire document. This can include updating the spelling, adding sentence numbers and adding part-of-speech tags

### Sentence tokenisation

A characteristic of historical texts is that sentence punctuation is inconsistent. In some documents a sentence may continue for several pages, with pauses marked by obliques. In other documents, sentence punctuation may be absent altogether.

Three different tokenisation models are provided:

* tokenise based on periods only
* tokenise based on periods, or a colon or oblique followed by a capital letter
* *tokenise based on a classification model (under construction)*

```python
doc.transform_tokenise_sentences(tokenisation_model="period")
doc.transform_tokenise_sentences(tokenisation_model="period_and_capital")
```

### Spelling correction

Most historical texts use spelling which we would describe as non-standard. While this can provide useful insights into diachronic language variation, sometime we need to apply a level of standardisation.

It is important to understand that this spelling correction does not alter the main tree structure. Updated orthographies are instead added to an `"orth"` attribute of a word (`<w>`) tag, for example

```xml
<w orth="the">y^e^</w>
```

A number of popular spelling corrections are provided out-of-the-box:

* remove asterisks from words such as *Frau\*n\*ce*
* remove carets from words such as *y^e^* (*the*)
* update v to u in words such as *vpon* (*upon*)
* update u to v in words such as *gaue* (*gave*)
* update l-bar to l in words such as *shaƚƚ* (*shall)*

```python
doc.transform_remove_asterisks()
doc.transform_ye_caret_to_the()
doc.transform_v_to_u()
doc.transform_u_to_v()
doc.transform_lbar_to_l()
```

Other spelling correction transformations can be built using the following functions, and supplying a pattern to be matched, and a replacement pattern:

```python
doc.update_spellings(match, replace)
doc.update_spellings_regex(match, replace)
```

### Numbering of sentences

Referencing of texts relies on sentence numbering. To automatically number each senetnce in a document incrementally (starting at 1 and going upwards), use:

```python
doc.transform_number_sentences()
```
It is recommended that any sentence tokenisation be completed before doing this.

### Sentence text

In the standard XML structure, words are attached to the `<w>` element. It can be helpful for human readability to have convenience text applied to a sentence element. You can add either the original text, or corrected text (if any spelling updates have been made), or both.

```python
doc.transform_add_original_text_to_sentences()
doc.transform_add_corrected_text_to_sentences()
```

This results in a structure like this:

```xml
<s orig-text="Once upon a time">
```

### Parsing and Part-of-Speech tags

NB this is experimental functionality and is not perfect at the moment. Parsing is done using spaCy's `en_core_web_md` model, which is based on Present Day English. This needs to be improved.

Before executing the parser, ensure that the `benepar` library is installed, and download the required ML model from the command line:

```bash
pip3 install benepar
python3 -m spacy download en_core_web_md
```

To parse a document, use:

```python
id = "MYTEXT"
doc.transform_parse(correctedText=True, add_parse_string=True, restructure=False, id)
```

It is recommended to make spelling updates and use the corrected Text for this process - this will be closer to the English which is expected by the parsing model.

You can add the parse string to the `<s>` tag as shown, or leave it out.

You can also choose to restructure the `<w>` tags within a sentence based on the parse. This will create nested phrase elements, `<phr>` as children of the sentence, and the `<w>` elements are added as children of those.

Part-of-speech tagging can only be done after parsing. This will add a `pos` attribute to each word with the relevant POS tag as its value.

```python
doc.transform_pos_tag()
```

## Worked example

This code will:
* import a document in CoLMEP format, setting a name and ID
* tokenise into sentences based on periods
* add sentence numbering
* run a number of spelling transforms
* get sentences as text and print them
* save as a new file

```python
import corpusparser

input_filename = "input.xml"
format = "colmep"

doc = corpusparser.Document.create_from_nonstandard_file(input_filename, format)
doc.set_name("My Historical Text")
doc.set_id("MYTEXT")

doc.transform_tokenise_sentences()
doc.transform_number_sentences()

doc.transform_remove_asterisks()
doc.transform_v_to_u()
doc.transform_u_to_v()
doc.transform_ye_caret_to_the()

sents = doc.get_sentences_as_text_list()
sents_filename = "sentences.txt"
try:
    with open(sents_filename, 'w') as f:
        for s in sents:
            f.write(s)
except IOError:
    print("IOError: Could not write to file " + sents_filename)

save_filename = "saved_work.xml"
doc.to_xml_file(save_filename, indent=2)
```
