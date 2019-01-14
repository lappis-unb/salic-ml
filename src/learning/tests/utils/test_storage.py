import os
import shutil
import unittest

from learning.utils import storage


class TestStorage(unittest.TestCase):
    TEST_FOLDER = ".test_folder/"
    TEST_FILE = os.path.join(TEST_FOLDER, "test_file.test")

    def setUp(self):
        self.has_error = False
        os.mkdir(TestStorage.TEST_FOLDER)

    def tearDown(self):
        shutil.rmtree(TestStorage.TEST_FOLDER)

    def test_save(self):
        data = "test"
        storage.save(TestStorage.TEST_FILE, data)

        self.assertTrue(os.path.isfile(TestStorage.TEST_FILE))

    def test_load(self):
        data = "test"
        storage.save(TestStorage.TEST_FILE, data)

        loaded_data = storage.load(TestStorage.TEST_FILE)

        self.assertEqual(data, loaded_data)

    def test_load_with_error(self):
        def error_callback():
            self.has_error = True

        storage.load(TestStorage.TEST_FILE, error_callback)

        self.assertTrue(self.has_error)
