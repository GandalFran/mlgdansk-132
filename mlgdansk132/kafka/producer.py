#!/usr/bin/python3
# Copyright 2022 Francisco Pinto-Santos
# See LICENSE for details.

import json
from typing import List, Any, Dict
from confluent_kafka import Producer
from mlgdansk132 import logger


class KafkaProducer:
    """Produces messages to Apache Kafka.

    Attributes:
        topics: set of topics to produce to.
        settings: Apache Kafka consumer configuration.
    """

    def __init__(self, topics: str, settings: dict):
        self._producer = None
        self._topics = topics
        self._settings = settings
        self.start()

    def delivery_report(self, err: Exception, msg: Any) -> None:
        """Error handler for message send.
        """

        if err is not None:
            logger.error(f"[delivery_report] error occurred during a message send {err}")

    def start(self) -> None:
        """Initializes the consumer
        """

        self._settings['on_delivery'] = self.delivery_report
        self._producer = Producer(self._settings)

    def stop(self) -> None:
        """Stops the consumer
        """

        self._producer.flush()

    def produce(self, data: Dict[str, Any]) -> None:
        """Produces a message to Apache Kafka given topics.
        
        Arguments:
            data: message to send.
        """

        try:
            data = json.dumps(data)
            for t in self._topics:
                self._producer.produce(t, value=data)
            self._producer.flush()
        except Exception as ex:
            logger.error(f"[write] error occurred on msg send {ex}")

    def flush(self) -> None:
        """Flushes the local message queue

        Forces the messages to be sent to Apache Kafka broker.
        """

        self._producer.flush()
