# Changelog
All notable changes to this project will be documented in this file.

The format is inpired from [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and the versiong aim to respect [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

Here is a template for new release sections

```
## [_._._] - 20XX-MM-DD

### Added
-
### Changed
-
### Removed
-
```
## [Unreleased]

### Added
- CHANGELOG.md
- CONTRIBUTING.md
- continuous integration with TravisCI (`.travis.yml`)
- linting tests and their config files (`.pylintrc` and `.flake8`)
- tests/ folder

### Changed
- fixed flake8 and pylint errors
- environnement.yml installs dependencies from requirements.txt so that conda is not required
