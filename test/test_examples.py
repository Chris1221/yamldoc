import unittest
import yamldoc
import sys
import io


class TestYAMLs(unittest.TestCase):
    def test_basic(self):
        entries = yamldoc.parse_yaml("test/yaml/basic.yaml", char="#'", debug=False)
        known_entries = [
            yamldoc.entries.Entry(
                key="meta", value='"Data"', meta="Here is some meta data."
            ),
            yamldoc.entries.Entry(
                key="fun",
                value="True",
                meta="And here is some more split over a couple of lines.",
            ),
        ]
        self.assertEqual(entries[0].key, known_entries[0].key)
        self.assertEqual(entries[0].value, known_entries[0].value)
        self.assertEqual(entries[0].meta, known_entries[0].meta)
        self.assertEqual(entries[1].key, known_entries[1].key)
        self.assertEqual(entries[1].value, known_entries[1].value)
        self.assertEqual(entries[1].meta, known_entries[1].meta)

        self.assertEqual(entries.__repr__(), '[YAML Entry [meta: "Data"]\n\t Meta: Here is some meta data., YAML Entry [fun: True]\n\t Meta: And here is some more split over a couple of lines.]')

    def test_two_level(self):
        entries = yamldoc.parse_yaml("test/yaml/two_level.yaml", char="#'", debug=False)
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0].key, "flat")
        self.assertEqual(entries[1].entries[0].key, "entry")

    def test_url_parsing(self):
        entries = yamldoc.parse_yaml("test/yaml/URLs.yaml", char="#'", debug=False)
        self.assertEqual(entries[0].value, "https://github.com/Chris1221/yamldoc")
        self.assertEqual(
            entries[1].entries[0].value, "https://github.com/Chris1221/yamldoc"
        )


class TestSchemas(unittest.TestCase):
    def test_basic(self):
        yaml = yamldoc.parse_yaml("test/yaml/basic.yaml", debug=False)
        schema, specials, extra = yamldoc.parser.parse_schema(
            "test/schema/basic.schema", debug=False
        )
        yamldoc.parser.add_type_metadata(schema, yaml)
        self.assertEqual(yaml[0].type, "string")
        self.assertEqual(yaml[1].type, "bool")

    def test_two_level(self):
        yaml = yamldoc.parse_yaml("test/yaml/two_level.yaml", debug=False)
        schema, specials, extra = yamldoc.parser.parse_schema(
            "test/schema/two_level.schema", debug=False
        )
        yamldoc.parser.add_type_metadata(schema, yaml)
        self.assertEqual(yaml[0].type, "string")
        self.assertEqual(yaml[1].entries[0].key, "entry")
        self.assertEqual(len(yaml[1].entries[0].type), 2)

    def test_complex(self):
        schema, specials, extra = yamldoc.parser.parse_schema(
            "test/schema/complex.schema", debug=False
        )
        self.assertTrue(schema["general"]["var1"] == ["array", "string"])
        self.assertTrue(schema["general"]["var2"] == "string")
        self.assertTrue(schema["general"]["var3"] == "string")


class TestMarkdown(unittest.TestCase):
    def test_basic(self):
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        _ = yamldoc.main(
            yaml_path="test/yaml/basic.yaml",
            schema_path="test/schema/basic.schema",
            footer=False,
        )
        output = new_stdout.getvalue()
        output = output.replace("<br />", " ")
        output = output.replace("\n", " ")
        sys.stdout = old_stdout
        proper_markdown = """# Configuration Parameters Reference\n\nAny information about this page goes here.\n\n| Key | Value | Type | Information |\n| :-: | :-: | :-: | :-- |\n| `meta` | `"Data"` | string | Here is some meta data. |\n| `fun` | `True` | bool | And here is some more split over a couple of<br />lines. |\n"""
        proper_markdown = proper_markdown.replace("<br />", " ")
        proper_markdown = proper_markdown.replace("\n", " ")
        print("\n\nActual Output:\n\n", output)
        print("\n\nExpected Output:\n\n", proper_markdown)

        self.assertTrue(output == proper_markdown)

    def test_two_level(self):
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        _ = yamldoc.main(
            yaml_path="test/yaml/two_level.yaml",
            schema_path="test/schema/two_level.schema",
            footer=False,
        )
        output = new_stdout.getvalue()
        # Lines are split by <br /> in the actual output but we don't care about where
        output = output.replace("<br />", "")
        output = output.replace("\n", "")
        sys.stdout = old_stdout
        proper_markdown = """# Configuration Parameters Reference\n\nAny information about this page goes here.\n\n| Key | Value | Type | Information |\n| :-: | :-: | :-: | :-- |\n| `flat` | `"yes"` | string | This is a flat entry. |\n\n\n\n## `two`\n\nBut this is a two level thing.\n\n### Member variables:\n\n| Key | Value | Type | Information |\n| :-: | :-: | :-: | :-- |\n| `entry` | `"hi"` | [\'string\', \'number\'] | These can have documentation too. |"""
        proper_markdown = proper_markdown.replace("<br />", "")
        proper_markdown = proper_markdown.replace("\n", "")
        print("\n\nActual Output:\n\n", output)
        print("\n\nExpected Output:\n\n", proper_markdown)

        self.assertTrue(output == proper_markdown)

    def test_simple_no_schema(self):
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        _ = yamldoc.main(
            yaml_path="test/yaml/basic.yaml",
            footer=False,
        )
        output = new_stdout.getvalue()
        output = output.replace("<br />", " ")
        output = output.replace("\n", " ")
        sys.stdout = old_stdout
        proper_markdown = """# Configuration Parameters Reference\n\nAny information about this page goes here.\n\n| Key | Value | Information |\n| :-: | :-: | :-: | :-- |\n| `meta` | `"Data"` | Here is some meta data. |\n| `fun` | `True` | And here is some more split over a couple of<br />lines. |\n"""
        proper_markdown = proper_markdown.replace("<br />", " ")
        proper_markdown = proper_markdown.replace("\n", " ")
        print("\n\nActual Output:\n\n", output)
        print("\n\nExpected Output:\n\n", proper_markdown)



if __name__ == "__main__":
    unittest.main()
