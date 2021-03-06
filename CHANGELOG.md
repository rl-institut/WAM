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
## [0.1.4] 2020-04-20

### Added
- Short link to Stemp-Tools on landing page
- Sphinx Makefile
- dynamic title for meta app lists

### Changed
- Removed unnecessary ionicon files
- Black style
- WAM installation instructions improved (esp. for Windows) #95
- Assumptions and sources are deleted if category is deleted (cascade)

### Security
- set django version to 2.2.10 

## [0.1.3] 2019-09-19

### Added
- I18N functionality via locale middleware enabled #76 #80
- enable support for markdownx extensions #83
- enable autodoc/APIdocs of WAM apps on ReadTheDocs #82

### Changed
- Highcharts source removed #78
- apps' icon size increased on landing page #89
- install docs extended: docker
- update README.md
- language in feedback form changed to EN #93

## [0.1.2] 2019-07-04

### Added
- CHANGELOG.md
- CONTRIBUTING.md
- continuous integration with TravisCI (`.travis.yml`)
- linting tests and their config files (`.pylintrc` and `.flake8`)
- tests/ folder
- add session error logging #64
- support custom id in InfoButton widget #63
- add feedback form #65
- add custom 404 and 500 error pages #70

### Changed
- fix flake8 and pylint errors
- environnement.yml installs dependencies from requirements.txt so that conda is not required
- fix grid-x layout error in InfoButton widget #66
- fix: avoid reimport of modules if multiple apps use the same #75

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
