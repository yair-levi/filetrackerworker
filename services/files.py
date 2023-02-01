import hashlib
import os
from os.path import join


class Files:
    def __init__(self, tracked_dir: str):
        self.tracked_dir = tracked_dir

    def get_md5(self, file_name: str):
        md5_hash = hashlib.md5()
        with open(join(self.tracked_dir, file_name), "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
        return md5_hash.hexdigest()

    def rename_duplicate_file(self, file_name: str):
        os.rename(join(self.tracked_dir, file_name), join(self.tracked_dir, file_name + "_DUP_#"))


