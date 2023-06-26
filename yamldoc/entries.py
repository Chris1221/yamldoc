import textwrap
from dataclasses import dataclass


def sanitize_meta(meta, char, exclude_char="#'!", override_exclude=False):
    """
    Sanitizes the meta information and indicates
    whether or not the entry should be excluded.

    Arguments:
        meta: The meta information to sanitize.
        override_exclude: Override the exclusion character and force inclusion.
    """

    meta = meta.lstrip().rstrip()

    if meta.startswith(exclude_char):
        exclude = True
    else:
        exclude = False

    if meta.startswith(exclude_char):
        meta = meta.replace(exclude_char, "").lstrip()
    elif meta.startswith(char):
        meta = meta.replace(char, "").lstrip()

    if override_exclude:
        exclude = False

    return meta, exclude


class MetaEntry:
    """
    A container to hold a base level YAML entry plus any associated
    hierarchical keys and values.
    """

    def __init__(self, name, meta, char, exclude_char="#'!", override_exclude=False):
        """
        Initialize the object.

        Arguments:
            name: Name of the value.
            meta: Comments derived from YAML file.
        """
        self.name = name
        self.char = char
        self.exclude_char = exclude_char
        self.isBase = True
        self.entries = []
        self.has_schema = False

        self.meta, self.exclude = sanitize_meta(meta, char, exclude_char, override_exclude)

    def is_list(self):
        """Returns True if all elements are list elements and False otherwise."""
        return all([isinstance(entry, ListElement) for entry in self.entries])

    def to_list_entry(self):
        """Converts this meta instance to a base level list entry."""
        if self.is_list():
            values = [entry.entry for entry in self.entries]
            entry = Entry(self.name, values, self.meta, self.char, self.exclude_char)
            
            # Small detail here, the meta has already been parsed
            # so we don't want to do it again.
            if self.exclude:
                entry.exclude = True

            return entry

    def __repr__(self):
        """
        Returns a print representation.
        """
        if self.has_schema:
            return (
                f"Meta object (n = {len(self.entries)}) with schema: {self.entries}" )
        else:
            return f"Meta object (n = {len(self.entries)}) without schema: {self.entries}"

    def non_excluded_entries(self):
        """Returns a list of entries that are not excluded."""
        return [entry for entry in self.entries if not entry.exclude]

    def table_header(self, schema=False):
        if schema:
            header = textwrap.dedent("""
            | Key | Value | Type | Information |
            | :-: | :-: | :-: | :-- |
            """)
        else:
            header = textwrap.dedent("""
            | Key | Value | Information |
            | :-: | :-: | :-- |
            """)

        return header
    
    def check_for_lists(self):
        new_entries = []
        for entry in self.entries:
            if isinstance(entry, MetaEntry):
                if entry.is_list():
                    new_entries.append(entry.to_list_entry())
                    continue
            new_entries.append(entry)
        
        self.entries = new_entries

    def to_markdown(self, schema=False):
        """
        Prints the contents of the object in markdown.

        Argumenets:
            schema: Print with four columns instead of three.
        """

        # If the object is excluded, we don't want to print anything.
        if self.exclude:
            return ""
        
        # Check for any sublists that need to be converted
        # from meta to entries
        self.check_for_lists()
        
        # Regardles of whether or not there are entries to print, we still want to print the
        # meta information.
        output = f"## `{self.name}`\n\n{self.meta.lstrip()}\n\n"

        # This is an early exit if there are no entries to print.
        entries_to_print = self.non_excluded_entries()
        if len(entries_to_print) == 0:
            output += "No member variables.\n\n"

            return output

        # So we have entries to print. Let's print them.
        output += "### Member variables:\n\n"
        output += self.table_header(schema)

        for entry in entries_to_print:
            output += entry.to_markdown(schema) + "\n"

        return output


@dataclass
class ListElement:
    entry: str
    exclude: bool = False 


class Entry:
    """
    Container for a single YAML key value pairing and associated metadata."""

    def __init__(
        self, key, value, meta, char="#'", exclude_char="#'!", override_exclude=False
    ):
        """
        Initialize the object

        Arguments:
           key: Name of the value
           value: Given value.
           meta: Any associated comments or meta data.
            char: Character to denote meta data.
            exclude_char: Character to denote exclusion.
            override_exclude: Override the exclusion character and force inclusion.
        """
        self.key = key
        self.value = value
        self.char = char
        self.exclude_char = exclude_char
        self.isBase = False
        self.type = None

        self.meta, self.exclude = sanitize_meta(
            meta, char, exclude_char, override_exclude
        )

    def __repr__(self):
        """
        Gives a print representation for the class.
        """
        if self.type is not None:
            return (
                f"YAML Entry [{self.key}: {self.value}]\n\t Meta: {self.meta}\n\t Type:"
                f" {self.type}"
            )
        else:
            return f"YAML Entry [{self.key}: {self.value}]\n\t Meta: {self.meta}"

    def to_markdown(self, schema=False):
        """
        Prints the entry as markdown.

        Arguments:
            schema: Print with four columns instead of three.
        """

        # If the entry is excluded, we don't want to print it.
        if self.exclude:
            return ""
        
        if schema:
            m = "<br />".join(textwrap.wrap(self.meta, width=50))
            if self.type == None:
                vartype = "Unknown"
            else:
                vartype = self.type
            return f"| `{self.key}` | `{self.value}` | {vartype} | {m} |"
        else:
            m = "<br />".join(textwrap.wrap(self.meta, width=50))
            return f"| `{self.key}` | `{self.value}` | {m} |"
