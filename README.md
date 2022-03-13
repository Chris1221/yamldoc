# Seamless auto-documentation of configuration parameters with yamldoc 

## Summary

Write this later. 

## Statement of need

For a tool to be reusable, maintainable, and approachable, transparent and up-to-date documentation is essential. While individual tools are able to automatically document their options in accessible web-pages with tools like Sphinx or MkDocs [1, 2], complex workflows written in workflow languages are not so straightforward to document. 
These complex computational workflows rely on large numbers of configuration parameters, often stored in a format which is readable by both machines and humans. One such format that has become popular is "YAML Ain’t Markup Language" (YAML) [3]. YAML is recommended by Red Hat as a configuration language due to its readability and user-friendliness. It is used across a large number of domains to document important configuration options. Examples include Kubernetes and Docker compose [4], continuous integration testing services like Travis-CI [5], Circle-CI [6], and Appveyor-CI [7], and large-scale bioinformatics workflow software like Snakemake [8]. As applications grow, the number of parameters to be included in the YAML does too. Currently, these configuration sets are mostly either undocumented or are done only in a haphazard way. Additionally, many software developers find it helpful to annotate their YAML configuration files with Schemas to ensure type safety, and there is no unified interface to allow for the documentation of a YAML configuration set and its associated schema [9]. In order to provide up-to-date, accurate reference material for users, there is a need for a tool that incorporates configuration parameters written in YAML into existing documentation engines. 


## Summary 


`yamldoc` provides a straightforward, dependency-free, and flexible method to knit documentation from YAML configuration files. Optionally, enforced types can be included from a linked Schema file. This method integrates seamlessly with documentation generation engines like Sphinx and ReadTheDocs to automatically document changes in configuration file parameters alongside the remainder of a software project. It adds very little overhead to continuously deployed documentation, even in the case of extremely long YAML files, and easily integrates with continuous deployment tools. 

`yamldoc` provides the ability for a developer to document YAML entries in-line with DOxygen-like syntax. It supports hierachical structuring of YAML parameters, and easily integrates schema files to allow for transparent typing of variables as functions change. 

As an example, all meta-data, or annotation, of YAML entries can be included directly before these entries in line with the entires. A special prefix character, here `#'` can be set with a command line option, and discriminates between information that should be knit and that which should not be knit. Entries and associated meta-data are parsed and printed in standard Markdown. This allows for simple interfacing with any documentation engine which can build from Markdown files.  

The following simple YAML document will be knit into **Table 1**. 
```
#' Here is some meta data.
meta: "Data"

#' And here is 
#' some more
#' split over
#' a couple of lines.
fun: True
```

> | Key | Value | Information |
> | :-: | :-: | :-- |
> | `meta` | `"Data"` | Here is some meta data. |
> | `fun` | `True` | And here is some more split over a couple of<br />lines. |
> ---
> Table 1: Tabular representation of parameter names, default options, and associated meta-data. 


## Philosophy and Implementation of Configuration Documentation 

* Give an example of a badly documented configuration file and then go onto how we fix this
* How we interface with schemas 

## Application to Snakemake workflows

* explain what snakemake is and how configuration files are recommended 

## Interfacing with Sphinx, Readthedocs, and Continuous Deployment services 

* How you can plug this into an auto doc frame work plus an example


## Future steps

- More prinipcled implementation would involve ANTLR4 syntax parsing to make this generalisable to JSON