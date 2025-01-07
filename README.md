[![Build Status](https://travis-ci.com/rl-institut/WAM.svg?branch=master)](https://travis-ci.com/rl-institut/WAM)
[![Documentation Status](https://readthedocs.org/projects/wam/badge/?version=latest)](https://wam.readthedocs.io/en/latest/?badge=latest)

**!!! This package is outdated and no longer maintained !!!**

2025-01-07 Installation fixed
- Pinned old package versions
- Do not load orphaned apps, restrict to StEmp tools by using
  `WAM_APPS=stemp_abw,stemp` in `docker-compose.yml`

___
<img align="right" width="150" src="https://github.com/rl-institut/WAM/blob/master/static/img/rli_logo.png">

# Web Applications & Maps (WAM)

WebAppMap-Server (WAM) provides a basic and expandable Django infrastructure to
easily add applications.

It is developed by the [Reiner Lemoine Institute](https://reiner-lemoine-institut.de/)
(RLI) and used on the [RLI WAM pages](https://wam.rl-institut.de/).

## Documentation

The documentation is available on [ReadTheDocs](https://wam.readthedocs.io).

## License

*Copyright (C) 2018 Reiner Lemoine Institut gGmbH*

GNU Affero General Public License v3.0

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
