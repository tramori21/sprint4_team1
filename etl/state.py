import json
from pathlib import Path
from datetime import datetime


class State:
    def __init__(self, file_path: str):
        self.file = Path(file_path)
        self.file.parent.mkdir(parents=True, exist_ok=True)
        if not self.file.exists():
            self._write({'modified': '1970-01-01T00:00:00'})

    def _read(self) -> dict:
        with self.file.open('r', encoding='utf-8') as f:
            return json.load(f)

    def _write(self, data: dict):
        with self.file.open('w', encoding='utf-8') as f:
            json.dump(data, f)

    def get_modified(self) -> datetime:
        value = self._read().get('modified')
        return datetime.fromisoformat(value)

    def set_modified(self, value: datetime):
        self._write({'modified': value.isoformat()})
