
from enum import Enum
from collections import namedtuple


AppInfo = namedtuple(
    'AppInfo',
    ['category', 'name', 'icon', 'url', 'url_arg'],
)
AppInfo.__new__.__defaults__ = (None, None)


class AppCategory(Enum):
    Web = 'web'
    App = 'app'
    Map = 'map'

    def label(self):
        return {
            AppCategory.Web: '<b>W</b>ebsites',
            AppCategory.App: '<b>A</b>pplications',
            AppCategory.Map: '<b>M</b>aps'
        }.get(self)

    def goto(self):
        return {
            AppCategory.Web: 'Zur Seite',
            AppCategory.App: 'Zum Tool',
            AppCategory.Map: 'Zur Karte'
        }.get(self)


class AppIcon(Enum):
    Map = 'img/icons_custom/Icon_map_w.png'
