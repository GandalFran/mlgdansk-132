#!/usr/bin/python3
# Copyright 2022 Francisco Pinto-Santos
# See LICENSE for details.

import re
import json
import time
import requests
import datetime
from typing import List, Dict, Any, Generator
import fasttext.util
from . import TweetSentiment
from . import Preprocessor
from mlgdansk132 import logger
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class TwitterSentimentAnalyzer:
    """Performs the tweets analysing.

    Attributes:
       extractor: SentimentIntensityAnalyzer extractor from Vader to analize the tweets
    """
    def __init__(self):
        self.extractor = SentimentIntensityAnalyzer()


    def analyze_tweet(self, tweet: object) -> Dict:
        """Analyze the tweet content and retrieves a dict with the information of the sentiment

        Args:
            tweet(:obj:`str`): contain the tweet with the info to analyse

        Returns:
            dict containing information about the sentiment of the tweet retrieved
        """

        try:
            #Clean the text
            t = Preprocessor(lang = 'en')
            text_analyze = t.clean(tweet['text'])

             #Analyse the sentiment
            #Collect the index labels and search the values for each sentiment
            polarity_scores = self.extractor.polarity_scores(text_analyze)

            #Convert from Python to JSON
            x = {
                "positive": str(polarity_scores['pos']),
                "negative": str(polarity_scores['neg']),
                "neutral": str(polarity_scores['neu']),
                "compound": str(polarity_scores['compound'])
            }
            return TweetSentiment(sentiment=json.dumps(x), date=tweet['date'])

        except Exception as e:
            logger.error(f"analysis error: {e}")
            time.sleep(10)
