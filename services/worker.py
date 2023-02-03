import json
from services.consumer import Consumer
import logging
from services.files import Files
from repository.files_repository import FileRepository


class Worker:
    def __init__(self, consumer: Consumer, file_repository: FileRepository, files_service: Files):
        self.consumer = consumer
        self.file_repository = file_repository
        self.files_service = files_service

    def worker(self, ch, method, properties, body):
        logging.info(f" [x] Received:   body:{body}")
        print(" [x] Received %r" % body)
        msg = json.loads(body)

        removed = msg.get("removed", None)
        added = msg.get("added", None)
        modified = msg.get("modified", None)

        if removed:
            for f in removed:
                self.removed_handler(f)
        if modified:
            for f in modified:
                self.modified_handler(f)
        if added:
            for f in added:
                self.added_handler(f)

        self.file_repository.close_transaction()

    def removed_handler(self, file_name: str):
        logging.info(f"file removed: {file_name}")
        self.file_repository.delete_file_by_name(file_name)

    def modified_handler(self, file_name: str):
        logging.info(f"file modified: {file_name} with new md5: {self.files_service.get_md5(file_name)}")

    def added_handler(self, file_name: str):
        logging.info(f"file added: {file_name}")
        md5_from_repository = self.files_service.get_md5(file_name)
        result_from_table = self.file_repository.find_by_md5(md5_from_repository)
        if len(result_from_table) > 0:
            self.files_service.rename_duplicate_file(file_name)
        else:
            self.file_repository.add_file(file_name=file_name, md5=md5_from_repository)

    def start(self):
        self.consumer.start_consume(callback=self.worker)
