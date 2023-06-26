### 0.1.5

#### March 25 2022

Fixed a weird untested bug for reading from meta-data file.

## [0.2.0](https://github.com/Chris1221/yamldoc/compare/0.1.6...v0.2.0) (2023-06-26)


### Features

* selectively exclude entries fix [#12](https://github.com/Chris1221/yamldoc/issues/12) ([#13](https://github.com/Chris1221/yamldoc/issues/13)) ([edf52f7](https://github.com/Chris1221/yamldoc/commit/edf52f7d1faf958426c2071f0fa51ada992d90ec))


### Bug Fixes

* allow for array-valued entries and fix sequential cases without meta-data; close [#6](https://github.com/Chris1221/yamldoc/issues/6), close [#10](https://github.com/Chris1221/yamldoc/issues/10) ([#11](https://github.com/Chris1221/yamldoc/issues/11)) ([06dae36](https://github.com/Chris1221/yamldoc/commit/06dae36d875d3e5b5fa7e07ad991e38f83882987))
* bug introduced in last push with spacing ([94da790](https://github.com/Chris1221/yamldoc/commit/94da790b7bf4ed5febc3788b3cd1c604f907f95b))
* evaluate decreasing indentation with multiple parents, close [#4](https://github.com/Chris1221/yamldoc/issues/4) ([9deae01](https://github.com/Chris1221/yamldoc/commit/9deae01ade043f143aec52fa5a0caaac7d313536))
* flush metadata after top level entry, close [#7](https://github.com/Chris1221/yamldoc/issues/7) ([6f5fd7c](https://github.com/Chris1221/yamldoc/commit/6f5fd7c87d6ee7eaaca8dc07a7b9aa9f0065e02d))
* remove extra white space from meta entries and between sections ([bc29d4a](https://github.com/Chris1221/yamldoc/commit/bc29d4a37303f051677de1e93a298075fc1e689b))

### 0.1.4
#### February 15 2020

Added support for enum valiation in schema file. These go into an "extra" data section of the YAML. Note that these have to be unpacked along with the other information now.

### 0.1.3
#### December 1 2020

Fixed parsing of URLs, the ":" delimiter was messing up the string splitting.
