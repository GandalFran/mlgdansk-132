#!/usr/bin/python3

# Copyright 2022 Francisco Pinto-Santos
# See LICENSE for details.



# Kafka configuration
KAFKA_BROKER = "deeptrends-04.der.usal.es:9092"

KAFKA_NUM_TRIES = 10
KAFKA_DELIVERY_TIMEOUT = 3000
KAFKA_INPUT_TOPICS = ['aws.ingest.fct.twitter.1']
KAFKA_PRODUCER_SETTINGS = {
    'retries': KAFKA_NUM_TRIES,
    'bootstrap.servers': KAFKA_BROKER,
    'default.topic.config': {
        'delivery.timeout.ms': KAFKA_DELIVERY_TIMEOUT
    }
}

KAFKA_GROUP_ID = "twitter-sentiment-processor 1"
KAFKA_OUTPUT_TOPICS = ['aws.twitter.fct.sentiment.1']
KAFKA_CONSUMER_SETTINGS = {
    'group.id': KAFKA_GROUP_ID,
    'bootstrap.servers': KAFKA_BROKER,
    'default.topic.config': {
        'auto.offset.reset': 'earliest',
        'max.poll.interval.ms':60000000

    }
}

KAFKA_STATUS_OUTPUT_TOPICS = ['aws.status.fct.track.1']

