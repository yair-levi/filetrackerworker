import pika
import logging


class Consumer:
    def __init__(self, host: str, port: int,  queue_name: str):
        self.host = host
        self.port = port
        self.queue_name = queue_name
        self.channel = None
        self._connect()

    def _connect(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)
        self.channel = channel

    def start_consume(self, callback):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()
        logging.info("[*] Waiting for messages.")

