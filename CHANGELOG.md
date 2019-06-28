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
- support custom id in InfoButton widget 

### Changed
- fix flake8 and pylint errors
- environnement.yml installs dependencies from requirements.txt so that conda is not required

## [0.1.1] 2019-05-22

### Added
- include highcharts in requirements.txt
- add StEmp-MV BETA icon for landing page to static files

### Changed
- fix a bug in the Dockerfile: requirements.txt was not copied into the tmp folder
- BETA icon for the WAM landing page


## [0.1.0] 2019-04-30

### Added
- CHANGELOG.md
- CONTRIBUTING.md
- LICENSE.md
- continuous integration with TravisCI (`.travis.yml`)
- linting tests and their config files (`.pylintrc` and `.flake8`)
- tests/ folder

### Changed
- fixed flake8 and pylint errors
- environment.yml installs dependencies
- if the environment variable WAM_CONFIG_PATH or WAM_APPS do not exist, the user is prompted with a meaningful error message
- if  WAM_APPS is an empty string, the app loads until the start page.