#!/usr/bin/env python
import json


class LocalJsonFile:
    """Class that implements CRUD for local file system."""

    def __init__(self, path):
        self.path = path

    def create(self, data):
        """Create and write a file or clobber a file."""
        with open(self.path, "w") as file:
            json.dump(data, file)

    def read(self):
        """Reads file to end."""
        with open(self.path, "r") as file:
            return json.load(file)

    def upsert(self, data):
        """Updates an existing file, or creates a new file. No clobber."""
        with open(self.path, "a") as file:
            json.dump(data, file)

    def delete(self):
        """Will permanently remove a file."""
        pass
