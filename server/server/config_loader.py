import os
import json
from django.conf import settings

class Config:
    config = {}

    @classmethod
    def load(cls, file_name='config.json'):
        try:
            full_path = os.path.join(settings.BASE_DIR, file_name)
            print(f"[Config] Loading from: {full_path}")

            with open(full_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            cls.config = data.get('config', {})
            print(f"[Config] Loaded keys: {list(cls.config.keys())}")

        except Exception as e:
            print(f"[Config ERROR]: {e}")
