import textwrap

class MetaEntry:
    def __init__(self, name, meta):
        self.name = name
        self.meta = meta
        self.isBase = True
        self.entries = []
        self.has_schema = False

    def __repr__(self):
        if self.has_schema:
            return f'YAML Meta Object with {len(self.entries)} entries [{self.name}] and type information.' 
        else:
            return f'YAML Meta Object with {len(self.entries)} entries [{self.name}]'

    def to_markdown(self, schema=False):
        if schema:
            output = f'## `{self.name}`\n\n{self.meta}\n\n'
            output += "### Member variables:\n\n"
            
            output += "| Key | Value | Type | Information |\n"
            output += "| :-: | :-: | :-: | :-- |\n"

            for entry in self.entries:
                output += entry.to_markdown(schema)
            output += "\n\n"
            return output

        else: 
            output = f'## `{self.name}`\n\n{self.meta}\n\n'
            output += "### Member variables:\n\n"
            
            output += "| Key | Value | Information |\n"
            output += "| :-: | :-: | :-- |\n"

            for entry in self.entries:
                output += entry.to_markdown()

            output += "\n\n"

            return output

        

class Entry:
    def __init__(self, key, value, meta):
        self.key = key
        self.value = value
        self.meta = meta
        self.isBase = False
        self.type = None

    def __repr__(self):
        if self.type is not None:
            return f'YAML Entry [{self.key}: {self.value}]\n\t Meta: {self.meta}\n\t Type: {self.type}'
        else:
            return f'YAML Entry [{self.key}: {self.value}]\n\t Meta: {self.meta}'

    def to_markdown(self, schema = False):
        if schema: 
            m = '<br />'.join(textwrap.wrap(self.meta, width = 50))
            if self.type == None:
                vartype = "Unknown"
            else:
                vartype = self.type
            return f'| `{self.key}` | `{self.value}` | {vartype} | {m} |\n'
        else:
            m = '<br />'.join(textwrap.wrap(self.meta, width = 50))
            return f'| `{self.key}` | `{self.value}` | {m} |\n'
