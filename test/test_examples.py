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
        entries = yamldoc.parse_yaml("test/yaml/basic.yaml", char = "#'", debug = False)
        known_entries = [
                yamldoc.entries.Entry(
                    key = "meta",
                    value = '"Data"',
                    meta = "Here is some meta data."),
                yamldoc.entries.Entry(
                    key = "fun",
                    value = "True",
                    meta = "And here is some more split over a couple of lines.")
                ]
        self.assertEqual(entries[0].key,known_entries[0].key)
        self.assertEqual(entries[0].value,known_entries[0].value)
        self.assertEqual(entries[0].meta,known_entries[0].meta)
        self.assertEqual(entries[1].key,known_entries[1].key)
        self.assertEqual(entries[1].value,known_entries[1].value)
        self.assertEqual(entries[1].meta,known_entries[1].meta)

    
    def test_two_level(self):
        entries = yamldoc.parse_yaml("test/yaml/two_level.yaml", char = "#'", debug = False)
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0].key, "flat")
        self.assertEqual(entries[1].entries[0].key, "entry")

    def test_url_parsing(self):
        entries = yamldoc.parse_yaml("test/yaml/URLs.yaml", char = "#'", debug = False)
        self.assertEqual(entries[0].value, "https://github.com/Chris1221/yamldoc")
        self.assertEqual(entries[1].entries[0].value, "https://github.com/Chris1221/yamldoc")
    
    def test_list_parsing(self):
        entries = yamldoc.parse_yaml("test/yaml/lists.yaml", char = "#'", debug = False)
        self.assertEqual(entries[0].value, ["1", "2", "3"])
        self.assertTrue(entries[0].meta.strip() == "List metadata")


class TestSchemas(unittest.TestCase):
    def test_basic(self):
        yaml = yamldoc.parse_yaml("test/yaml/basic.yaml", debug = False)
        schema, specials, extra = yamldoc.parser.parse_schema("test/schema/basic.schema", debug = False)
        yamldoc.parser.add_type_metadata(schema, yaml)
        self.assertEqual(yaml[0].type, "string")
        self.assertEqual(yaml[1].type, "bool")

    def test_two_level(self):
        yaml = yamldoc.parse_yaml("test/yaml/two_level.yaml", debug = False)
        schema, specials, extra = yamldoc.parser.parse_schema("test/schema/two_level.schema", debug = False)
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
        schema, specials, extra = yamldoc.parser.parse_schema("test/schema/complex.schema", debug = False)
        self.assertTrue(schema["general"]["var1"] == ["array", "string"])
        self.assertTrue(schema["general"]["var2"] == "string")
        self.assertTrue(schema["general"]["var3"] == "string")

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

    


if __name__ == '__main__':
    unittest.main()

