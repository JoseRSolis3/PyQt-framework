from kafka import KafkaProducer, KafkaConsumer
import json
from log_util import advanced_log

def producer_builder(host, topic, tvalue, key, partition, ):
    if host is None:
        advanced_log("warning",f"Please enter a host location.")
    elif isinstance(host, (str, int)):
        advanced_log("info",f"Confirmed! Returning host location.")
        producer = KafkaProducer(
            bootstrap_servers=[host],
            value_serializer = lambda v: json.dumps(v).encode("utf-8")
        )
    else:
        advanced_log("warning",f"Invalid data type. Please try again.")
    
    if topic is None:
        advanced_log("warning",f"Topic is empty please try again.")
    elif isinstance(topic, str):
        advanced_log("info",f"Confirmed! Returning topic name.")
        topic = topic.strip().lower()
    else:
        advanced_log("warning","Invalid data type. Please try again.")