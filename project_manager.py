import os
from pathlib import Path
from database import LogDatabase

class ProjectManager:
    def __init__(self, base_dir="projects"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)

    def create_project(self, name: str):
        """Creates a new project folder with its database and logs folder"""
        project_path = self.base_dir / name
        logs_path = project_path / "logs"
        db_path = project_path / "db.json"

        logs_path.mkdir(parents=True, exist_ok=True)
        db = LogDatabase(db_path)

        print(f"✅ Project '{name}' created at {project_path}")
        return db

    def get_project_db(self, name: str):
        """Return a database handler for an existing project"""
        project_path = self.base_dir / name
        db_path = project_path / "db.json"
        if not db_path.exists():
            raise FileNotFoundError(f"❌ Project '{name}' does not exist.")
        return LogDatabase(db_path)

    def list_projects(self):
        """List all available projects"""
        return [p.name for p in self.base_dir.iterdir() if p.is_dir()]
