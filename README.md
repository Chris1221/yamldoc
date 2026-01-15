

## Documentation Engine for YAML

[![PyPI version](https://badge.fury.io/py/yamldoc.svg)](https://badge.fury.io/py/yamldoc) [![CircleCI](https://dl.circleci.com/status-badge/img/gh/Chris1221/yamldoc/tree/master.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/Chris1221/yamldoc/tree/master) [![codecov](https://codecov.io/gh/Chris1221/yamldoc/branch/master/graph/badge.svg?token=OpQhpILdh3)](https://codecov.io/gh/Chris1221/yamldoc) [![Downloads](https://pepy.tech/badge/yamldoc)](https://pepy.tech/project/yamldoc)

This package converts a YAML file into markdown, formatting values and associated metadata in a `doxygen`-like way. To get started, check out the [documentation](http://chrisbcole.me/yamldoc/) and [tutorials](http://chrisbcole.me/yamldoc/tutorial/).

## Installation

```sh
pip install yamldoc
```

This will install the python package, which contains a command line interface `yamldoc`. To see usage instructions, invoke the `--help` flag:

```sh
yamldoc -h
```

## Features and Supported Syntax 

`yamldoc` does not support the full syntax of YAML, which is vast and complex. Instead, it supports a subset of YAML that is useful for documenting configuration files. This subset includes:

| Syntax | Supported | Description |
| --- | --- | --- |
| `key: value` | Yes | Basic key-value pairs. Values can be any type and are not subject to coercion. (i.e. `yes` will remain `yes` in `yamldoc` output. It will not be coerced to `True` as a YAML parser would. The goal of `yamldoc` is to be **transparent**, not feature complete. |
| `key: [value1, value2, ...]` | Yes | Arrays are understood by yamldoc if they are either listed on one line or each entry given on a new line with dashes to indicate entries. |
| Comments | Yes | Non-`yamldoc` comments are ignored. `yamldoc` comments are indicated by a special character (default `#'`) at the beginning of the line. `yamldoc` comments can be broken over as many lines as you like, they will be added together when the markdown is constructed. |

Things YAML does not support: 

- Nested arrays past two levels of nesting. `yamldoc` will not parse nested arrays past two levels of nesting. [Issue #14](https://github.com/Chris1221/yamldoc/issues/14) tracks this request. 
- Multi-line strings (unquoted or quoted scalars) indicated by `|` or `>` are not supported.
- Lists of dictionaries are not supported.
- Multiple documents in a single file are supported, but no special handling is done to separate them. It is assumed that each document is a separate configuration file.
- Complex mapping keys starting with `!!` or `?` are not supported. `yamldoc` will not parse complex mappings, tags, or explicit tags. 


## Philosophy

Many programs and utilities use YAML ([YAML Ain't Markup Language](https://en.wikipedia.org/wiki/YAML)) as a human and machine readable interface to configuration parameters and other values. More broadly, many kinds of data can be stored in YAML with minimal effort from the user. However, often a configuration file accumulates a highly specific set of configurations marked up with vague, difficult to interpret comments. It is the goal of this package to provide an easy interface for developers to document data in their YAML files as well as the expected types from a [JSON YAML schema validator](https://json-schema-everywhere.github.io/yaml). Doing so will allow a transparent interface between the developer's expectations and the user's configurations. 

### Specific Application to Snakemake

This package was designed specifically to document the possible configuration options of a [Snakemake](https://snakemake.readthedocs.io/en/stable/) pipeline. In this application, the developer of the pipeline encodes many different specific options that the user may configure at run time, but these are often poorly documented. When they are, it is easy for the documentation to fall out of sync with the actual options in the configuration file. `yamldoc` automatically documents all configuration paramters as well as taking types from a schema file. The package will also read any comments that are present above each paramter and insert them into a parameter table for easy reference.

For more details on using YAML to configure Snakemake pipelines, see [here](https://snakemake.readthedocs.io/en/stable/snakefiles/configuration.html).

## Example Files

For a minimal example of `yamldoc`, see the files in `/test/yaml` and `/test/schema`.

## Usage

For a basic report, point the command line interface to a YAML file.

```sh
yamldoc test/yaml/basic.yaml
```

You can also include type information from a schema file.

```sh
yamldoc test/yaml/basic.yaml -s test/schema/basic.schema
```

## Other Options

`yamldoc` defaults to using `#'` as a special marker, but you can choose this character yourself if you wish. Just set it on the command line at parse-time:

```sh
yamldoc test/yaml/basic.yaml -c "YOURCHAR"
```

`yamldoc` also includes support for certain special declarations in the schema file. Right now these include:

- `_yamldoc_title`: This specifies the overall title of the markdown page generated.
- `_yamldoc_description`: A description to follow the title. 

These are picked out of the schema file and reported. 

`yamldoc` has support for skipping individual entries in the reported markdown. Note this is seperate from adding comments that are not meta-data, these are respected and never reported. Skipping refers to actual entries in the YAML file. To skip an entry, add the skip character (by default, `#'!`) to the beginning of the line. 

```yaml
# This is a comment, it will not be reported
#' This entry will be included in the report 
entry1: value1

#'! This entry will be skipped
entry2: value2
```
