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

## Examples

```sh
yamldoc test/yamltwo_level.yaml
```

Outputs:

> # Configuration Parameters Reference
> Any information about this page goes here.
> | Key | Value | Information |
> | :-: | :-: | :-- |
> | `flat` | `"yes"` | This is a flat entry. |
> ## `two`
> But this is a two level thing.
> ### Member variables:
> | Key | Value | Information |
> | :-: | :-: | :-- |
> | `entry` | `"hi"` | But this is a two level thing. These can have<br />documentation too. |

