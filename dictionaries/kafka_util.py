from confluent_kafka import Producer, Consumer
from api_util import Check
from log_util import advanced_log
import json

class Library():
    def __init__(self):
        self.linkDirectory = {}
        self.producerDirectory = {}

    def linkRegistry(self, linkName: str, link : str):
        self.linkDirectory[linkName] = link
    
    def producerRegistry(self, linkName: str, producer: str):
        self.producerDirectory[linkName] = producer

    def topicRegistry(self,linkName: str, topicName: str, values: dict):
        Check.none(linkName, topicName, values)
        Check.String(linkName, topicName)
        Check.Dictionary(values)
        producer = self.producerDirectory[linkName]
        producer.send(topicName, values)
        producer.flush()

    def search(self, startsWith: str):
        Check.none(startsWith)
        Check.String(startsWith)
        startsWith = startsWith.strip().lower()
        return{
            name: self.linkDirectory[name]
            for name in self.linkDirectory
            if name.startswith(startsWith)
        }

    def ping(self, linkName: str):
        Check.none(linkName)
        Check.String(linkName)
        if linkName in self.producerDirectory:
            producer = self.producerDirectory[linkName]
            try:
                if producer.bootstrap_connected():
                    return True
                return False
            except Exception as e:
                raise SystemError(f"Kafka ping failed: {e}")


class kafkaProducer():
    def __init__(self) -> None:
        self.lib = Library()
        self.producer = None

    def create(self, host: str, port: int, linkName: str):
        """
            Creates a Kafka producer and registers it under a linkName.

            Args:
                host (str): Kafka host
                port (int): Kafka port
                linkName (str | None): Identifier for this producer connection

            Returns:
                self: Allows method chaining        
        """
        Check.none(host, port, linkName)
        Check.String(host, linkName)
        Check.Number(port)
        self.bootstrap = f"{host}:{port}"
        self.producer = Producer({'bootstrap.servers': self.bootstrap})
        if linkName is not None:
            if linkName in self.lib.search(linkName):
                raise NameError(f"Error: {linkName} already exists!")
            if self.bootstrap in self.lib.search(self.bootstrap):
                raise ValueError(f"Error: {port} is already assigned.")
            self.lib.linkRegistry(linkName, self.bootstrap)
            self.lib.producerRegistry(linkName, self.producer)
        return self
            
                