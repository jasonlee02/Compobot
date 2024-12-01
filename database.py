import json
import os

class JsonDB:
    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(os.path.join(os.getcwd(), filename)):
            with open(filename, "w") as f:
                json.dump({}, f)
            self.file_handler = open(filename, "r+")
        else:
            self.file_handler = open(filename, "r+")
        
        self.json = json.load(self.file_handler)

    def dump(self):
        self.file_handler.seek(0)
        json.dump(self.json, self.file_handler)
        self.file_handler.truncate()

    def get(self, user_id):
        if user_id not in self.json:
            self.json[user_id] = 100
            self.dump()
        return self.json[user_id]
    
    def set(self, user_id, value):
        self.json[user_id] = value
        self.dump()

if __name__ == "__main__":
    database = JsonDB("data.json")
    database.set("1", 1)
    print(database.get("1"))