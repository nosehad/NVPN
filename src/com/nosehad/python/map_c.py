class Map:
    def __init__(self):
        self.storage = []

    def add(self, key, value):
        self.storage.append([key, value])

    def get_raw(self):
        return self.storage

    def get_by_index(self, index):
        return self.storage[index][1]

    def contains(self, key):
        for item in self.storage:
            if item[0] == key:
                return True
            
        return False

    def set(self, key, value):
        for item in self.storage:
            if item[0] == key:
                item[1] = value

    def get(self, key):
        for item in self.storage:
            if item[0] == key:
                return item[1]

        return None

    def remove(self, key):
        for item in self.storage:
            if item[0] == key:
                self.storage.remove([key, item[1]])
