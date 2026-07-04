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

        self.type = None
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

    def to_table_row(self, schema=False):
        """Render this MetaEntry as a single table row for display inside a parent table."""
        if self.exclude:
            return ""
        m = "<br />".join(textwrap.wrap(self.meta.lstrip(), width=50))
        if schema:
            vartype = self.type if self.type is not None else "object"
            return f"| `{self.name}` |  | {vartype} | {m} |"
        else:
            return f"| `{self.name}` |  | {m} |"

    def to_markdown(self, schema=False, depth=1):
        """
        Prints the contents of the object in markdown.

        Arguments:
            schema: Print with four columns instead of three.
            depth: Nesting depth; controls heading levels (1=##/###, 2=####/#####).
        """

        if self.exclude:
            return ""

        self.check_for_lists()

        section_level = depth * 2
        members_level = depth * 2 + 1

        # CommonMark caps heading levels at h6; fall back to bold text beyond that
        if section_level <= 6:
            section_header = f"{'#' * section_level} `{self.name}`"
        else:
            section_header = f"**`{self.name}`**"

        if members_level <= 6:
            members_header = f"{'#' * members_level} Member variables:"
        else:
            members_header = "**Member variables:**"

        output = f"{section_header}\n\n{self.meta.lstrip()}\n\n"

        entries_to_print = self.non_excluded_entries()
        if len(entries_to_print) == 0:
            output += "No member variables.\n\n"
            return output

        output += f"{members_header}\n\n"
        output += self.table_header(schema)

        nested_meta_entries = []
        for entry in entries_to_print:
            if isinstance(entry, MetaEntry):
                output += entry.to_table_row(schema) + "\n"
                nested_meta_entries.append(entry)
            else:
                output += entry.to_markdown(schema) + "\n"

        for entry in nested_meta_entries:
            output += "\n\n\n" + entry.to_markdown(schema, depth=depth + 1)

        return output


@dataclass
class ListElement:
    entry: str
    exclude: bool = False

    def to_markdown(self, schema=False):
        if schema:
            return f"| `{self.entry}` |  | Unknown |  |"
        else:
            return f"| `{self.entry}` |  |  |"


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
