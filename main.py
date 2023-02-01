import logging

import yaml
from services.consumer import Consumer
from services.worker import Worker
from repository.files_repository import FileRepository
from services.files import Files


def read_configuration():
    with open("config.yml", "r") as config:
        cfg = yaml.safe_load(config)
    return cfg


if __name__ == '__main__':
    configuration = read_configuration()
    logging.basicConfig(filename='fileTracker.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)
    rabit_mq_host = configuration["rabitMQ"]["host"]
    rabit_mq_port = configuration["rabitMQ"]["port"]
    queue_name = configuration["rabitMQ"]["queue_name"]
    directory = configuration["directory"]
    db_name = configuration["db_name"]
    file_repository = FileRepository(db_name=db_name)
    file_repository.create_table_if_not_exists()
    file_repository.close_transaction()
    files = Files(tracked_dir=directory)
    consumer = Consumer(host=rabit_mq_host, port=rabit_mq_port,  queue_name=queue_name)
    worker = Worker(consumer=consumer, file_repository=file_repository, files_service=files)
    worker.start()
