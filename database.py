from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import hashlib
import json

class LogDatabase:
    def __init__(self, db_path):
        # Initialize a TinyDB database with caching
        self.db = TinyDB(db_path, storage=CachingMiddleware(JSONStorage))
        self.table = self.db.table("logs")

    def _hash_entry(self, entry):
        """
        Creates a unique hash of a log entry based on its contents.
        This helps us detect duplicates even if the same file is parsed again.
        """
        # Convert to JSON string with sorted keys for stable hashing
        entry_str = json.dumps(entry, sort_keys=True)
        return hashlib.sha256(entry_str.encode()).hexdigest()

    def bulk_insert(self, entries):
        """
        Insert multiple logs into the database while avoiding duplicates.
        """
        if not entries:
            print("⚠️ No entries to insert.")
            return

        # Get existing hashes for fast deduplication
        existing_hashes = {i.get("hash") for i in self.table.all()}
        new_entries = []

        for e in entries:
            h = self._hash_entry(e)
            if h not in existing_hashes:
                e["hash"] = h
                new_entries.append(e)

        if new_entries:
            self.table.insert_multiple(new_entries)
            print(f"✅ Inserted {len(new_entries)} new log entries.")
        else:
            print("ℹ️ No new logs inserted (all duplicates).")

    def get_all(self):
        """Return all logs in this project's database."""
        return self.table.all()

    def filter_by(self, field, value):
        """Filter logs by a specific field (like process, pid, etc.)."""
        Log = Query()
        return self.table.search(Log[field] == value)
