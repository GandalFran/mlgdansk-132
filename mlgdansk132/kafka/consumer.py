#!/usr/bin/python3
# Copyright 2022 Francisco Pinto-Santos
# See LICENSE for details.

import json
from typing import List, Any
from confluent_kafka import Consumer, Message


class KafkaConsumer:
    """Consumes messages from Apache Kafka.

    Attributes:
        topics: set of topics to listen to.
        settings: Apache Kafka consumer configuration
        poll_timeout: Apache Kafka polling timeout for requesting messages.
    """

    def __init__(self, topics: str, settings: dict, poll_timeout: float = 1.0) -> None:
        self._consumer = None
        self._topics = topics
        self._settings = settings
        self._poll_timeout = poll_timeout
        self.start()

    def start(self) -> None:
        """Initializes the consumer
        """

        self._consumer = Consumer(self._settings)
        self._consumer.subscribe(self._topics)

    def stop(self) -> None:
        """Stops the consumer
        """

        self._consumer.close()

    def consume(self, min_messages: int = 1) -> List[dict]:
        """Consumes a message

        Args:
            min_messages: minimun number of messages to consume

        Returns:
            retrieved messages
        """

        messages = []
        while len(messages) < min_messages:
            msg = self._read_one()
            if msg is not None:
                messages.append({
                    'topic': msg.topic(),
                    'msg': json.loads(msg.value().decode('UTF-8'))
                })
        return messages

    def _read_one(self) -> Message:
        """Reads one message from Apache Kafka.

        Returns:
            a message in the format of the Apache Kafka library.
        """

        while True:
            try:
                msg = self._consumer.poll(self._poll_timeout)
                if msg is not None:
                    if not msg.error():
                        return msg
            except Exception as ex:
                return None
