## Documentation Engine for YAML

[![CircleCI](https://circleci.com/gh/Chris1221/yamldoc.svg?style=svg&circle-token=114ff93a4850a6cf03289d1b7a9aaf4af351afc9)](https://app.circleci.com/pipelines/github/Chris1221/yamldoc?branch=master) [![codecov](https://codecov.io/gh/Chris1221/yamldoc/branch/master/graph/badge.svg?token=OpQhpILdh3)](https://codecov.io/gh/Chris1221/yamldoc)

This package converts a YAML file into markdown, formatting values and associated metadata in a `doxygen`-like way.  

## Installation

```sh
git clone git@github.com:Chris1221/yamldoc.git
pip install yamldoc
```

This will install the python package, which contains a command line interface `yamldoc`.

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
