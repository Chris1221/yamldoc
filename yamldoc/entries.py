class Entry:
    def __init__(self, key, value, meta):
        self.key = key
        self.value = value
        self.meta = meta

    def __repr__(self):
        return f'YAML Entry [{self.key}: {self.value}]\n\t Meta: {self.meta}'
