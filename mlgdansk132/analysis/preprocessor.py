#!usr/bin/python

# Copyright 2022 Francisco Pinto-Santos
# See LICENSE for details.


import re
import nltk
import spacy
from textblob import TextBlob
from nltk.corpus import stopwords
from stop_words import get_stop_words
from typing import Any, List, Pattern, Dict


class Preprocessor:
    """Preprocess a text
    
    Args:
        lang: language used to analyze the text.
    Attributes:
        LANGUAGE_MAPPINGS: the available mappings
        LANGUAGE_COMMON_NAMES: the long name of given languages
        PATTERNS: regular expressions to detect various elements such as URLs, mentions, emails, numbers, emojis, etc
    """

    LANGUAGE_MAPPINGS = {
        'es': 'es_core_news_sm',
        'en': 'en_core_web_sm'
    }

    LANGUAGE_COMMON_NAMES = {
        'en': 'english',
        'es': 'spanish'
    }

    PATTERNS: Dict[str, Pattern[str]] = {
        'multiple_spaces': re.compile(' +'),
        'text_shortener': re.compile(r"(.)\1{3,}"),
        'url': re.compile(r'https?://[\w./\-?=&+]+'),
        'mentions': re.compile(r'((?<=\W)|^)(@\w+)(\s*@\w+)*'),
        'email': re.compile(r'[\w.+-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z0-9-]+'),
        'number': re.compile(r'[0-9]+'),
        'emoji': re.compile("[" \
                            + "\U0001F600-\U0001F64F" # Emoticons
                            + "\U0001F300-\U0001F5FF" # Symbols & Pictograms
                            + "\U0001F680-\U0001F6FF" # Transport 
                            + "\U0001F1E0-\U0001F1FF" # Flags 
                            + "]+", flags=re.UNICODE)
    } 

    def __init__(self, lang: str = 'en') -> None:

        if lang not in Preprocessor.LANGUAGE_MAPPINGS:
            raise ValueError(f'The given language ({lang}) is not avilable in the language mappings: {",".join(list(Preprocessor.LANGUAGE_MAPPINGS.keys()))}')

        self.lang = lang
        self.nlp = spacy.load(Preprocessor.LANGUAGE_MAPPINGS[lang])

        # build stopwords
        stopwords = list(get_stop_words(lang))
        spacy_stopwords = list(self.nlp.Defaults.stop_words)
        nltk_stopwords = list(nltk.corpus.stopwords.words(Preprocessor.LANGUAGE_COMMON_NAMES[lang]))
        self.stopwords = set(stopwords + spacy_stopwords + nltk_stopwords)

    def low(self, text: str) -> str:
        """Lowers a text
        Args:
            text: element to process
        Returns: 
            text in lower
        """ 

        return text.lower()
         
    def reduce_lengthening(self, text: str) -> str:
        """Reduces the text length
        Args:
            text: element to process
        Returns: 
            text with reduced length
        """
        
        text = Preprocessor.PATTERNS['text_shortener'].sub(r"\1\1\1", text)
        return text
         
    def remove_punctuation(self, text: str, min_token_length:int = 2) -> str:
        """Cleans the text from punctuation, small words, etc
        Args:
            text: element to process
            min_token_length: the minimum length that a token must have to be conserved
        Returns: 
            text withouth punctunation, small words, etc
        """

        # transform punctuation into spaces
        punctuation = '!"#$%&\'()*+-‘’/<=>?[\\]^_`{|}~”“'
        spaces = ' ' * len(punctuation)
        text = text.translate(str.maketrans(punctuation, spaces))

        # clean document
        document = self.nlp(text)
        filtered_tokens = [token for token in document if not token.is_punct]
        filtered_tokens = [token for token in filtered_tokens if len(token) > min_token_length and token.text.isalpha()]

        # join again the document
        precleaned_text = ' '.join(str(token.text) for token in filtered_tokens)
        return precleaned_text
 
    def remove_stopwords(self, text: str) -> str:
        """ Removes stopwords
        Args:
            text: element to process
        Returns: 
            text without stopwords
        """
    
        # remove stopwords        
        stripped_text = TextBlob(text).words
        text_withouth_stopwords = [word for word in stripped_text if word not in self.stopwords]

        # join text
        text_withouth_stopwords = ' '.join(text_withouth_stopwords)
        return text_withouth_stopwords
     
    def clean(self, text: str) -> str:
        """ Applys preprocessing to the text
        Concretelly removes URL, mentions, emails, emojis, numbers, punctuation symbols, etc. also reduces
        the text lenghtening, and removes stopwords among others.
        Args:
            text: element to process
        Returns: 
            text preprocessed
        """

        # replace URLs, Users, Emojis, etc.
        text = Preprocessor.PATTERNS['url'].sub('URL', text)
        text = Preprocessor.PATTERNS['mentions'].sub('USER', text)
        text = Preprocessor.PATTERNS['email'].sub('MAIL', text)
        text = Preprocessor.PATTERNS['emoji'].sub(r'', text)
        text = Preprocessor.PATTERNS['number'].sub(r'', text)

        # apply text processings
        # text = self.low(text)
        text = self.reduce_lengthening(text)
        text = self.remove_punctuation(text)
        # text = self.remove_stopwords(text)

        # replace multiple spaces per one
        text = Preprocessor.PATTERNS['multiple_spaces'].sub(' ', text)

        return text
