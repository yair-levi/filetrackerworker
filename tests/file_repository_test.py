import hashlib
import unittest
from repository.files_repository import FileRepository
from pathlib import Path


class TestFilesRepository(unittest.TestCase):

    def setUp(self) -> None:
        self.db_name = Path('test_db')
        self.repository = FileRepository(db_name=str(self.db_name.resolve()))
        self.repository.create_table_if_not_exists()

    def tearDown(self):
        self.repository.conn.close()
        self.db_name.unlink()

    def test_add_file_and_find_by_md5(self):
        self.repository.add_file("test1", "d41d8cd98f00b204e9800998ecf8427e")
        result_from_db = self.repository.find_by_md5("d41d8cd98f00b204e9800998ecf8427e")
        file_name = result_from_db[0][0]
        file_md5 = result_from_db[0][1]

        # Assert
        self.assertEqual(file_name, "test1")
        self.assertEqual(file_md5, "d41d8cd98f00b204e9800998ecf8427e")

    def test_update_md5_by_file_name(self):
        self.repository.add_file("test1", "d41d8cd98f00b204e9800998ecf8427e")
        self.repository.update_md5_by_file_name("test1", "d41d8cd98f00b204e9800998ecf81234")
        result_from_db = self.repository.find_by_md5("d41d8cd98f00b204e9800998ecf81234")
        file_name = result_from_db[0][0]
        file_md5 = result_from_db[0][1]

        # Assert
        self.assertEqual(file_name, "test1")
        self.assertEqual(file_md5, "d41d8cd98f00b204e9800998ecf81234")

    def test_delete_file_by_name(self):
        self.repository.add_file("test1", "d41d8cd98f00b204e9800998ecf8427e")
        self.repository.delete_file_by_name("test1")
        result_from_db = self.repository.find_by_md5("d41d8cd98f00b204e9800998ecf8427e")

        # Assert
        self.assertFalse(len(result_from_db) > 0)
