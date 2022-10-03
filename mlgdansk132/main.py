#!/usr/bin/python3
# Copyright 2022 Francisco Pinto-Santos
# See LICENSE for details.

from time import sleep
from datetime import datetime
import uuid

from mlgdansk132 import config
from mlgdansk132 import logger
from mlgdansk132.kafka import KafkaConsumer
from mlgdansk132.kafka import KafkaProducer
from mlgdansk132.analysis import TwitterSentimentAnalyzer

# kafka producers and consumers
consumer = KafkaConsumer(config.KAFKA_INPUT_TOPICS,
                         config.KAFKA_CONSUMER_SETTINGS)
producer = KafkaProducer(config.KAFKA_OUTPUT_TOPICS,
                         config.KAFKA_PRODUCER_SETTINGS)
producer_status = KafkaProducer(config.KAFKA_STATUS_OUTPUT_TOPICS,
                                config.KAFKA_PRODUCER_SETTINGS)
# extractors
analysis = TwitterSentimentAnalyzer()


def behaviour():

    # Read requests
    messages = consumer.consume()
   
    for message in messages:

        # Treat request
        request_id = message['msg']['request-id']
        tweet = message['msg']['tweet']

        # Manage data
        logger.info(f"Processing request {request_id}")

        # Just the text is necessary for the analysis
        tweet = tweet
        tweetSentiment = analysis.analyze_tweet(tweet)

        # Send extracted tweets sentiments
        producer.produce({
            'request-id': request_id,
            'content-id': tweetSentiment.uuid,
            'document-content': tweetSentiment.sentiment,
            'date': tweetSentiment.date
        })
        
        logger.info(f"Finished request {request_id}")

        # Create status info
        logger.info(f"Processing status request {request_id}")
        producer_status.produce({
        })
        logger.info(f"Finished status request {request_id}")

def run():
    while True:
        behaviour()


if __name__ == '__main__':
    run()
