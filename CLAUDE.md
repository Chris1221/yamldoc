# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`yamldoc` is a Python package that converts YAML files into markdown documentation. It extracts metadata comments (prefixed with `#'` by default) and formats them into doxygen-style documentation tables. The package is designed for documenting configuration files, particularly Snakemake pipeline configurations.

**Key Features:**
- Parses YAML files with special metadata comments (default: `#'`)
- Supports optional JSON schema validation for type information
- Generates markdown tables with key, value, type, and metadata columns
- Handles nested structures (up to 2 levels deep)
- Supports entry exclusion via prefix character (default: `#'!`)

## Commands

### Installation and Development
```bash
# Install Pixi (if not already installed)
curl -fsSL https://pixi.sh/install.sh | bash

# Install all dependencies and the package
pixi install

# The yamldoc CLI is available via the entrypoint
pixi run yamldoc --help
```

### Testing
```bash
# Run all tests
pixi run test

# Run tests with pytest
pixi run test-pytest

# Run with coverage
pixi run test-coverage
```

### Usage
```bash
# Basic usage - generate markdown from YAML
pixi run yamldoc test/yaml/basic.yaml

# With schema file for type information
pixi run yamldoc test/yaml/basic.yaml -s test/schema/basic.schema

# Custom metadata character
pixi run yamldoc test/yaml/basic.yaml -c "YOURCHAR"

# With debug output
pixi run yamldoc test/yaml/basic.yaml -d

# Override exclusion character
pixi run yamldoc test/yaml/basic.yaml -e "#!!" --override-exclude
```

## Architecture

### Core Components

**[yamldoc/parser.py](yamldoc/parser.py)**: Main parsing engine
- `parse_yaml()`: Line-by-line parser that identifies metadata comments and key-value pairs
- `parse_schema()`: Extracts type information from JSON schema files
- `add_type_metadata()`: Merges schema type information into parsed YAML entries
- `main()`: Orchestrates parsing and markdown generation

**[yamldoc/entries.py](yamldoc/entries.py)**: Data structures
- `Entry`: Single key-value pair with metadata
- `MetaEntry`: Base-level entry with hierarchical sub-entries (the `isBase` attribute distinguishes these)
- `ListElement`: Individual list item
- Each class has `to_markdown()` methods for output generation

**[yamldoc/cli.py](yamldoc/cli.py)**: Command-line interface using argparse

### Parsing Logic

The parser is stateful and works as follows:

1. **Line-by-line processing**: Reads YAML file sequentially, tracking indentation levels
2. **Metadata accumulation**: Lines starting with the metadata character (`#'`) accumulate until a key-value pair is found
3. **Entry creation**: When a key-value pair is encountered, creates an `Entry` or `MetaEntry` with accumulated metadata
4. **Hierarchical handling**: `MetaEntry` objects (when `key:` has no value) collect sub-entries until indentation returns to level 0
5. **List detection**: `MetaEntry` objects with only `ListElement` children are converted to `Entry` objects with array values

**Important**: The parser tracks state via `current_entry` and flushes entries when returning to base indentation level.

### Schema Integration

Schema files follow JSON schema format with yamldoc-specific extensions:
- `_yamldoc_title`: Sets markdown page title
- `_yamldoc_description`: Sets page description
- Type information from `type:` fields is extracted and matched to YAML entries by key name

### Exclusion Feature

Entries can be excluded from documentation:
- Lines starting with exclude character (`#'!` by default) mark the following entry as excluded
- `exclude` attribute is set to `True` on the entry
- `to_markdown()` methods return empty string for excluded entries
- `--override-exclude` flag forces inclusion of all entries

## Limitations

The parser intentionally supports a YAML subset, NOT full YAML spec:
- Maximum 2 levels of nesting for arrays
- No multi-line strings (`|` or `>`)
- No lists of dictionaries
- No complex mapping keys or tags (`!!`, `?`)
- Values are transparent (no type coercion): `yes` stays `yes`, not converted to `True`

## Testing Structure

Tests in [test/test_examples.py](test/test_examples.py) are organized by test class:
- `TestYAMLs`: Parser correctness for different YAML structures
- `TestSchemas`: Schema parsing and type metadata integration
- `TestE2E`: End-to-end tests using `get_output()` helper
- `TestMarkdown`: Exact markdown output validation

Test files in [test/yaml/](test/yaml/) and [test/schema/](test/schema/) provide fixtures.
