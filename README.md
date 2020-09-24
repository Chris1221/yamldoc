## Documentation Engine for YAML

This package converts a YAML file into markdown, formatting values and associated metadata in a `doxygen`-like way.  

## Installation

```sh
git clone git@github.com:Chris1221/yaml.doc.git
pip install yaml.doc/
```

This will install both the python package, and the command line interface `yamldoc`.

## Usage

Point the command line interface to a YAML file.

```sh
yamldoc test/yaml/basic.yaml
```

For additional options see 

```sh
yamldoc -h
```

For example:

```yaml
#' Simple key-value pair.
entry: 1

#' Hierarchical entries are also supported.
big_entry:
    #' Along with documentation for sub entries.
    sub_entry: 1
```

Becomes:

> ### `entry`: `1`
>	Simple key-value pair.
>
> ## `big_entry`
>	Hierarchical entries are also supported
>
> ### `sub_entry`: `1`
>	Along with documentation for sub entries.
