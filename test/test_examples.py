import unittest
import yamldoc

class TestExampleYAMLs(unittest.TestCase):
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



if __name__ == '__main__':
    unittest.main()

