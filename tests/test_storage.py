import unittest
import json
from src.storage import LocalJsonFile
from unittest.mock import patch, mock_open, MagicMock
from src.constants import LOCAL_FILE_STORE_PATH, LOCAL_FILE_STORE_NAME


class TestStorage(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestStorage, self).__init__(*args, **kwargs)
        self.path = f"{LOCAL_FILE_STORE_PATH}{LOCAL_FILE_STORE_NAME}"
        self.storage_provider = LocalJsonFile(self.path)

    @patch("json.dump", MagicMock(return_value="{cool}"))
    @patch("builtins.open", new_callable=mock_open)
    def test_create(self, mock_file):
        self.storage_provider.create("{cool}")
        json.dump.assert_called_once()
        mock_file.assert_called_with(self.path, "w")

    @patch("builtins.open", new_callable=mock_open, read_data='[{"data": "ian"}]')
    def test_read(self, mock_file):
        assert self.storage_provider.read() == [{"data": "ian"}]
        mock_file.assert_called_with(self.path, "r")

    @patch("json.dump", MagicMock(return_value="{cool}"))
    @patch("builtins.open", new_callable=mock_open)
    def test_upsert(self, mock_file):
        self.storage_provider.upsert("{cool}")
        json.dump.assert_called_once()
        mock_file.assert_called_with(self.path, "a")

    # def test_delete(self):
    #     pass
