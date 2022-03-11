# Seamless auto-documentation of configuration parameters with yamldoc 

## Introduction

Configuration is a key part of complex workflows. Parameter values that might otherwise be passed at the command line are stored for posterity in human and machine readable formats. One format which has recently become popular for this purpose across diverse application areas is Yet Another Markup Language (YAML). 

YAML configurations can be found in many different tool sets (web applications, CLI tools often store config in .rc files, pipelines for bioinformatics). As applications grow, the number of parameters to be included in the YAML does too. Currently, these configuration sets are mostly documented only in a haphazard way, if at all, and there is no interface between the inline documentation and required types from schema files. 

Yamldoc solves this problem by directly interfacing with autodocumentation engines in readthedocs, sphinx, etc. to create elegant tables that summarise parameters, their types, and their default values. The software is light, dependency-free, and easily integrates with automated building engines like Github Actions, CircleCI, and Travis CI.

## Philosophy and Implementation of Configuration Documentation 

* Give an example of a badly documented configuration file and then go onto how we fix this
* How we interface with schemas 

## Application to Snakemake workflows

* explain what snakemake is and how configuration files are recommended 

## Interfacing with Sphinx, Readthedocs, and Continuous Deployment services 

* How you can plug this into an auto doc frame work plus an example
