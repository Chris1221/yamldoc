import unittest
import yamldoc
import yaml
import sys
import io

def check_boolean_cooercion(value, output):
    """Checks that the boolean cooercion works as expected"""
    if value:
        assert "yes" in output
    elif not value:
        assert "no" in output
    else:
        raise AssertionError

def assert_all_printed(input, output):
    with open(input) as f:
        data = yaml.safe_load(f)

    # get all the data keys from the yaml file
    keys = list(data.keys())

    # assert that all the keys are in the output
    for key in keys:
        assert key in output

    # make sure all the values are there 
    for key in keys:
        if isinstance(data[key], list):
            for value in data[key]:
                assert str(value) in output
        elif isinstance(data[key], dict):
            for value in data[key].values():
                # "yes" and "no" get coersed to True and False
                # so we need to check for both
                try:
                    assert str(value) in output
                except AssertionError:
                    check_boolean_cooercion(value, output)
        
        elif isinstance(data[key], str):
            assert data[key] in output
        elif isinstance(data[key], bool):
            try:
                assert str(data[key]) in output
            except AssertionError:
                check_boolean_cooercion(data[key], output)
        elif isinstance(data[key], int):
            assert str(data[key]) in output
        elif isinstance(data[key], float):
            assert str(data[key]) in output
        else:
            print(f"Unknown type {type(data[key])} for {key}")
            print("Please add this type to the test suite, unsure how to handle it.")

    return True

def get_output(path:str, schema=None) -> str:
    """Retrieves output of YAMLDOC"""
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    _ = yamldoc.main(
        yaml_path=path,
        schema_path=schema,
    )
    output = new_stdout.getvalue()
    sys.stdout = old_stdout

    return output


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
        self.assertEqual(entries[1].entries[0].value, "https://github.com/Chris1221/yamldoc")
    
    def test_list_parsing(self):
        entries = yamldoc.parse_yaml("test/yaml/lists.yaml", char = "#'", debug = False)
        self.assertEqual(entries[0].value, ["1", "2", "3"])
        self.assertTrue(entries[0].meta.strip() == "List metadata")

    def test_deeper_nesting(self):
        entries = yamldoc.parse_yaml("test/yaml/deeper_nesting.yaml", char="#'", debug=False)
        self.assertEqual(len(entries), 3)
        self.assertEqual(entries[0].key, "flat")
        self.assertEqual(entries[1].entries[0].key, "entry")
        self.assertEqual(entries[2].entries[0].key, "level_two")
        self.assertEqual(entries[2].entries[0].entries[0].key, "level_three")

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

    def test_lists(self):
        yaml = yamldoc.parse_yaml("test/yaml/lists.yaml", debug = False)
        schema, specials, extra = yamldoc.parser.parse_schema("test/schema/lists.schema", debug = False)
        yamldoc.parser.add_type_metadata(schema, yaml)
        self.assertEqual(yaml[0].value, ["1", "2", "3"])
        self.assertTrue(yaml[0].meta.strip() == "List metadata")
        self.assertTrue(yaml[0].type == "array")

    def test_complex(self):
        schema, specials, extra = yamldoc.parser.parse_schema(
            "test/schema/complex.schema", debug=False
        )
        self.assertTrue(schema["general"]["var1"] == ["array", "string"])
        self.assertTrue(schema["general"]["var2"] == "string")
        self.assertTrue(schema["general"]["var3"] == "string")

    def test_deeper_nesting(self):
        yaml = yamldoc.parse_yaml("test/yaml/deeper_nesting.yaml", debug=False)
        schema, specials, extra = yamldoc.parser.parse_schema(
            "test/schema/deeper_nesting.schema", debug=False
        )
        yamldoc.parser.add_type_metadata(schema, yaml)
        self.assertEqual(yaml[0].type, "string")
        self.assertEqual(yaml[1].entries[0].key, "entry")
        self.assertEqual(yaml[2].entries[0].key, "level_two")
        self.assertEqual(yaml[2].entries[0].entries[0].key, "level_three")
        self.assertEqual(yaml[2].entries[0].entries[0].type, "string")

class TestE2E(unittest.TestCase):
    def test_basic(self):
        output = get_output("test/yaml/basic.yaml", "test/schema/basic.schema")
        self.assertTrue(assert_all_printed("test/yaml/basic.yaml", output))
    
    def test_two_level(self):
        output = get_output("test/yaml/two_level.yaml", "test/schema/two_level.schema")
        self.assertTrue(assert_all_printed("test/yaml/two_level.yaml", output))

    def test_lists(self):
        output = get_output("test/yaml/lists.yaml", "test/schema/lists.schema")
        self.assertTrue(assert_all_printed("test/yaml/lists.yaml", output))

    def test_url(self):
        output = get_output("test/yaml/URLs.yaml")
        self.assertTrue(assert_all_printed("test/yaml/URLs.yaml", output))

    def test_long(self):
        output = get_output("test/yaml/long.yaml")
        self.assertTrue(assert_all_printed("test/yaml/long.yaml", output))

    def test_deeper_nesting(self):
        output = get_output("test/yaml/deeper_nesting.yaml", "test/schema/deeper_nesting.schema")
        self.assertTrue(assert_all_printed("test/yaml/deeper_nesting.yaml", output))


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

        self.assertTrue(output == proper_markdown)

    def test_deeper_nesting(self):
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        _ = yamldoc.main(
            yaml_path="test/yaml/deeper_nesting.yaml",
            schema_path="test/schema/deeper_nesting.schema",
            footer=False,
        )
        output = new_stdout.getvalue()
        # Lines are split by <br /> in the actual output but we don't care about where
        output = output.replace("<br />", "")
        output = output.replace("\n", "")
        sys.stdout = old_stdout
        proper_markdown = """# Configuration Parameters Reference\n\nAny information about this page goes here.\n\n| Key | Value | Type | Information |\n| :-: | :-: | :-: | :-- |\n| `flat` | `"yes"` | string | This is a flat entry. |\n\n\n\n## `two`\n\nBut this is a two level thing.\n\n### Member variables:\n\n| Key | Value | Type | Information |\n| :-: | :-: | :-: | :-- |\n| `entry` | `"hi"` | [\'string\', \'number\'] | These can have documentation too. |\n\n\n\n## `three`\n\nThis is a three level thing.\n\n### Member variables:\n\n| Key | Value | Type | Information |\n| :-: | :-: | :-: | :-- |\n| `level_two` |  | object | This is the second level. |\n\n\n\n#### `level_two`\n\nThis is the second level.\n\n##### Member variables:\n\n| Key | Value | Type | Information |\n| :-: | :-: | :-: | :-- |\n| `level_three` | `"hello"` | string | This is the third level. |"""
        proper_markdown = proper_markdown.replace("<br />", "")
        proper_markdown = proper_markdown.replace("\n", "")
        print("\n\nActual Output:\n\n", output)
        print("\n\nExpected Output:\n\n", proper_markdown)

        self.assertTrue(output == proper_markdown)


if __name__ == "__main__":
    unittest.main()
