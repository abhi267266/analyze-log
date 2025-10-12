from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import hashlib
import json
from pathlib import Path
import shutil


class ProjectDatabase:
    def __init__(self, project_name):
        self.project_name = project_name
        self.db_path = Path("projects") / project_name / "db.json"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db = TinyDB(self.db_path, storage=CachingMiddleware(JSONStorage))
        self.table = self.db.table("projects")

    def _hash_entry(self, entry):
        """Compute SHA256 hash of a log entry."""
        entry_str = json.dumps(entry, sort_keys=True)
        return hashlib.sha256(entry_str.encode()).hexdigest()

    def _hash_file(self, file_content):
        """Compute SHA256 hash of a file content."""
        return hashlib.sha256(file_content.encode()).hexdigest()

    def create_or_update_project(self, log_type, logs, file_content=None, important_logs=None, summary=None):
        """
        Create or update a project document.
        If file_content is provided, skip updating if the file has been processed.
        """
        important_logs = important_logs or []
        file_hash = self._hash_file(file_content) if file_content else None

        Project = Query()
        existing = self.table.get(Project.project_name == self.project_name)

        if existing:
            # Load existing hashes
            processed_files = existing.get("processed_files", [])
            existing_log_hashes = {self._hash_entry(log) for log in existing.get("all_logs", [])}

            # Skip if this file has been processed
            if file_hash and file_hash in processed_files:
                print(f"⚠️ File already processed. Skipping update for project '{self.project_name}'.")
                return

            # Only add new logs
            new_logs = [log for log in logs if self._hash_entry(log) not in existing_log_hashes]
            all_logs = existing.get("all_logs", []) + new_logs

            # Merge important logs
            important_logs = [log for log in all_logs if log.get("level") in ["ERROR", "WARNING", "CRITICAL"]]

            # Update processed files
            if file_hash:
                processed_files.append(file_hash)

            # Update the project document
            project_doc = {
                "project_name": self.project_name,
                "log_type": log_type,
                "all_logs": all_logs,
                "important_logs": important_logs,
                "summary": summary,
                "processed_files": processed_files
            }
            self.table.update(project_doc, Project.project_name == self.project_name)
            print(f"✅ Project '{self.project_name}' updated with {len(new_logs)} new log entries.")
        else:
            # New project
            project_doc = {
                "project_name": self.project_name,
                "log_type": log_type,
                "all_logs": logs,
                "important_logs": important_logs,
                "summary": summary,
                "processed_files": [file_hash] if file_hash else []
            }
            self.table.insert(project_doc)
            print(f"✅ Project '{self.project_name}' created with {len(logs)} log entries.")

        self.db.close()

    def get_project(self):
        Project = Query()
        return self.table.get(Project.project_name == self.project_name)

    def delete_project(self):
        self.db.close()
        project_folder = self.db_path.parent
        if project_folder.exists():
            shutil.rmtree(project_folder)
            print(f"✅ Project '{self.project_name}' deleted.")
