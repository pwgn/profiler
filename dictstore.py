from bson import json_util
import json

class DictStore:
    def __init__(self, filename):
        self.filename = filename
        try:
            with open(self.filename) as f:
                self.store = json.load(f, object_hook=json_util.object_hook)
        except FileNotFoundError:
            self.store = {}

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.store, f, default=json_util.default)

    def get(self, key):
        return self.store.get(key, None)

    def set(self, key, value):
        self.store[key] = value
        self.save()