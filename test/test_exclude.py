import markdown as md
import yamldoc


def test_simple_exclusion():
    yaml = yamldoc.parse_yaml(
        "test/yaml/exclusion/simple_exclusion.yaml", exclude_char="#'!"
    )

    assert len(yaml) == 2, "Both entries should be included."

    entry1, entry2 = yaml

    assert entry1.key == "key1", "Entry 1 should be included."
    assert entry2.key == "key2", "Entry 2 should be included."

    assert entry1.exclude == False, "Entry 1 should not be excluded."
    assert entry2.exclude == True, "Entry 2 should be excluded."

    assert entry1.value == "Data", "Entry 1 should have value 'value1'."
    assert entry2.value == "True", "Entry 2 should have value 'value2'."


def test_complex_exclusion():
    yaml = yamldoc.parse_yaml(
        "test/yaml/exclusion/complex_exclusion.yaml", exclude_char="#'!"
    )

    assert len(yaml) == 9, "All entries should be included."

    excluded = [entry for entry in yaml if entry.exclude]
    assert len(excluded) == 2, "Two entries should be excluded."

    # The last one is a subentry, so we need to get that one

    meta_entries = [entry for entry in yaml if hasattr(entry, "name")]
    assert len(meta_entries) == 5, "There should be 7 meta entries."

    entry1, entry2, entry3, entry4, entry5 = meta_entries

    for e in entry1, entry2, entry3, entry5:
        assert e.exclude == False, "Entry should not be excluded."

    assert entry5.entries[0].exclude == True, "Entry should be excluded."
    assert entry5.entries[1].exclude == False, "Entry should not be excluded."
