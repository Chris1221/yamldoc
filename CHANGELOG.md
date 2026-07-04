### 0.1.5

#### March 25 2022

Fixed a weird untested bug for reading from meta-data file.

## [0.4.0](https://github.com/Chris1221/yamldoc/compare/v0.3.8...v0.4.0) (2026-07-04)


### Features

* support nested objects ([#18](https://github.com/Chris1221/yamldoc/issues/18)) ([fdccf8a](https://github.com/Chris1221/yamldoc/commit/fdccf8a277c316f9c951c347fd484a0d06d1a4cb))


### Bug Fixes

* render ListElement in mixed lists with empty key column ([f7b908d](https://github.com/Chris1221/yamldoc/commit/f7b908dd4f7786d3f3f180446cbf22553f891b0f))
* skip ListElement objects when rendering mixed MetaEntry to avoid crash ([01f4ec9](https://github.com/Chris1221/yamldoc/commit/01f4ec94f2c5ca73726042adead581b32fdc81c1))
* strip list dash prefix from sub-entry keys and render ListElement as key with no value ([ec06ce5](https://github.com/Chris1221/yamldoc/commit/ec06ce5b6177c8bea78fd600a058f1469e785ec7))

## [0.3.8](https://github.com/Chris1221/yamldoc/compare/v0.3.7...v0.3.8) (2026-07-04)


### Bug Fixes

* skip ordinary comments in parser to avoid crash on lines without colon ([4a38301](https://github.com/Chris1221/yamldoc/commit/4a3830159c443d2828a2913f2569d7906e2ebfc7))


### Documentation

* note minimum pip version requirement in README ([228ba00](https://github.com/Chris1221/yamldoc/commit/228ba008057f7f37fb227c8e0d3c84b429cb0959))

## [0.3.7](https://github.com/Chris1221/yamldoc/compare/v0.3.6...v0.3.7) (2026-07-04)


### Bug Fixes

* trigger release-please ([dd1fe1d](https://github.com/Chris1221/yamldoc/commit/dd1fe1db98b10c43c384c7082438ee839e3680af))

## [0.3.6](https://github.com/Chris1221/yamldoc/compare/v0.3.5...v0.3.6) (2026-07-04)


### Bug Fixes

* another check: ([a9d27cc](https://github.com/Chris1221/yamldoc/commit/a9d27cc89d10b2eec40748a826cae267533f7338))

## [0.3.5](https://github.com/Chris1221/yamldoc/compare/v0.3.4...v0.3.5) (2026-07-04)


### Bug Fixes

* trigger again ([20b7726](https://github.com/Chris1221/yamldoc/commit/20b7726514fc535ae11f9a88dad17a61c5ab06ca))

## [0.3.4](https://github.com/Chris1221/yamldoc/compare/v0.3.3...v0.3.4) (2026-07-04)


### Bug Fixes

* trigger release-please ([27e60a6](https://github.com/Chris1221/yamldoc/commit/27e60a66680bd9b69e38a0357b52e6705f8f66ce))

## [0.3.3](https://github.com/Chris1221/yamldoc/compare/v0.3.2...v0.3.3) (2026-07-03)


### Bug Fixes

* trigger release-please ([214dbd9](https://github.com/Chris1221/yamldoc/commit/214dbd9717e5b08f2fda655bcbb3612e2c53d94d))

## [0.3.2](https://github.com/Chris1221/yamldoc/compare/v0.3.1...v0.3.2) (2026-07-03)


### Bug Fixes

* trigger release-please ([7090fd3](https://github.com/Chris1221/yamldoc/commit/7090fd3c2bd76b8e7eac6eea05f583ea8474a4ab))

## [0.3.1](https://github.com/Chris1221/yamldoc/compare/v0.3.0...v0.3.1) (2026-07-03)


### Bug Fixes

* require setuptools&gt;=61 for PEP 621 pyproject.toml support ([cc307d1](https://github.com/Chris1221/yamldoc/commit/cc307d1a68ba9cc2dca5e9a15bf42a8c109efee6))

## [0.3.0](https://github.com/Chris1221/yamldoc/compare/v0.2.0...v0.3.0) (2026-06-14)


### Features

* upgrade to pixi ([#19](https://github.com/Chris1221/yamldoc/issues/19)) ([cd1db32](https://github.com/Chris1221/yamldoc/commit/cd1db329a1d0b9d573208f2a7a7226216a621b7f))


### Bug Fixes

* remove setuptools_scm to fix pip install from source ([#22](https://github.com/Chris1221/yamldoc/issues/22)) ([9082c42](https://github.com/Chris1221/yamldoc/commit/9082c42199beff9e910b82c9afa4ec9a70a5684d))

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
