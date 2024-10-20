"""Producer base-class providing common utilites and functionality"""
import logging
import time


from confluent_kafka import avro
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.avro import AvroProducer

logger = logging.getLogger(__name__)

SCHEMA_REGISTRY_URL = "http://localhost:8081"
BROKER_URL = "PLAINTEXT://localhost:9092"


class Producer:
    """Defines and provides common functionality amongst Producers"""

    # Tracks existing topics across all Producer instances
    existing_topics = set([])

    def __init__(
        self,
        topic_name,
        key_schema,
        value_schema=None,
        num_partitions=1,
        num_replicas=1,
    ):
        """Initializes a Producer object with basic settings"""
        self.topic_name = topic_name
        self.key_schema = key_schema
        self.value_schema = value_schema
        self.num_partitions = num_partitions
        self.num_replicas = num_replicas

        #
        #
        # TODO: Configure the broker properties below. Make sure to reference the project README
        # and use the Host URL for Kafka and Schema Registry!
        #
        #
        self.broker_properties = {
            "bootstrap.servers" : BROKER_URL,
            "schema.registry.url" : SCHEMA_REGISTRY_URL
        }

        # If the topic does not already exist, try to create it
        if self.topic_name not in Producer.existing_topics:
            self.create_topic()
            Producer.existing_topics.add(self.topic_name)

        # TODO: Configure the AvroProducer
            self.producer = AvroProducer(self.broker_properties,
                                         default_key_schema=self.key_schema,
                                         default_value_schema=self.value_schema)
        

    def create_topic(self):
        """Creates the producer topic if it does not already exist"""
        #
        #
        # Write code that creates the topic for this producer if it does not already exist on
        # the Kafka Broker.
        #
        client = AdminClient({"bootstrap.servers": BROKER_URL})
        # check if this topic already exists
        topics_metadata = client.list_topics(timeout=10)
        if self.topic_name not in topics_metadata.topics.values(): # does not already exists
            futures = client.create_topics(
                [NewTopic(topic=self.topic_name, num_partitions=5, replication_factor=1)])
            
            for _, future in futures.items():
                try:
                    future.result()
                except Exception as e:
                    print("exiting production loop")


    def time_millis(self):
        return int(round(time.time() * 1000))

    def close(self):
        """Prepares the producer for exit by cleaning up the producer"""
        #
        #
        #  Write cleanup code for the Producer here
        #
        #
        self.producer.flush()

    def time_millis(self):
        """Use this function to get the key for Kafka Events"""
        return int(round(time.time() * 1000))
