class MetaEntry:
    def __init__(self, name, meta):
        self.name = name
        self.meta = meta
        self.isBase = True
        self.entries = []

    def to_markdown(self):
        output = f'## `{self.name}`\n\n{self.meta}\n\n'
        for entry in self.entries:
            output += entry.to_markdown()

        return output
        

class Entry:
    def __init__(self, key, value, meta):
        self.key = key
        self.value = value
        self.meta = meta
        self.isBase = False

    def __repr__(self):
        return f'YAML Entry [{self.key}: {self.value}]\n\t Meta: {self.meta}'

    def to_markdown(self):
        return f'### `{self.key}`: `{self.value}`\n\n{self.meta}\n\n'
