#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv


storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    print("This is db engine")
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    print("This is file storage engine")
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
