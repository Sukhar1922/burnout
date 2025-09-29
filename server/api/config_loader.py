import json
import os


class Config:
    config = {}

    @classmethod
    def load(cls, file_name='config.json'):
        try:
            full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), file_name)

            with open(full_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            cls.config = data.get('config', {})

        except Exception as e:
            print(f"[Config ERROR]: {e}")
