## Documentation Engine for YAML

This package converts a YAML file into markdown, formatting values and associated metadata in a `doxygen`-like way.

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

> # `entry`: `1`
>	Simple key-value pair.
