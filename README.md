## Documentation Engine for YAML

[![PyPI version](https://badge.fury.io/py/yamldoc.svg)](https://badge.fury.io/py/yamldoc) [![CircleCI](https://circleci.com/gh/Chris1221/yamldoc.svg?style=svg&circle-token=114ff93a4850a6cf03289d1b7a9aaf4af351afc9)](https://app.circleci.com/pipelines/github/Chris1221/yamldoc?branch=master) [![codecov](https://codecov.io/gh/Chris1221/yamldoc/branch/master/graph/badge.svg?token=OpQhpILdh3)](https://codecov.io/gh/Chris1221/yamldoc) [![Downloads](https://pepy.tech/badge/yamldoc)](https://pepy.tech/project/yamldoc)

This package converts a YAML file into markdown, formatting values and associated metadata in a `doxygen`-like way. To get started, check out the [documentation](http://chrisbcole.me/yamldoc/) and [tutorials](http://chrisbcole.me/yamldoc/tutorial/).

## Installation

```sh
pip install yamldoc
```

This will install the python package, which contains a command line interface `yamldoc`. To see usage instructions, invoke the `--help` flag:

```sh
yamldoc -h
```


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
