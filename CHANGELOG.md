# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Types of changes:

- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Deprecated` for soon-to-be removed features.
- `Removed` for now removed features.
- `Fixed` for any bug fixes.
- `Security` in case of vulnerabilities.

## [Unreleased]

## [0.3.4] - 2021-06-05

### Changed

- Moved from Travis CI to GitHub actions for tests/CI.
- Moved to src layout.
- Moved setup.py config to setup.cfg.
- Added pyproject.toml file.
- Removed .isort.cfg.
- Make tomlkit an optional dependency.

## [0.3.3] - 2020-07-11

### Added

- Added a function `parameter_sweep` to generate multiple config files for parameter sweeps.

## [0.3.2] - 2019-09-24

### Added

- Add comments to TOML format.
- Add name and filepath attributes.

### Changed

- Moved parsers to a separate module.

## [0.3.1] - 2019-09-11

### Added

- Add type annotations to functions.
- Add parser for nested dictionaries.

## [0.3.0] - 2019-09-03

### Added

- Add support for TOML files.

## [0.2.1] - 2019-08-26

### Added

- Add continuous integration for tests.

### Changed

- Remove NumPy as a dependency.
- Drop support for Python 3.5 or earlier.

## [0.2.0] - 2019-08-26

### Added

- Add installation instructions in README.
- Add `__header__` and `__datetime__` special keys for comments in Phantom config files.

## [0.1.0] - 2019-08-22

- Initial release.
