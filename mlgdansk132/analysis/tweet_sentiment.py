#!/usr/bin/python3

# Copyright 2022 Francisco Pinto-Santos
# See LICENSE for details.

import uuid
from typing import Dict
import datetime


class TweetSentiment:
    """Model of a tweet´s sentiment.

    Attributes:
        uuid: unique identifier of the tweet´s sentiment.
        sentiment: the tweet´s sentiment.
    """
    def __init__(self, sentiment: str, date: datetime.datetime) -> None:
        self.uuid = str(uuid.uuid4())
        self.sentiment = sentiment
        self.date = date

    def __dict__(self) -> Dict[str, str]:

        return {'sentiment': self.sentiment, 'date': self.date}