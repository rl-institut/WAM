from enum import Enum
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


class AppInfo:
    def __init__(self, category, name, url, closed=False, icon=None, url_arg=None):
        self.category = category
        self.name = name
        self.__url = url
        self.closed = closed
        self.icon = icon
        self.__url_arg = url_arg

    @property
    def url(self):
        try:
            if self.__url_arg is None:
                url = reverse(self.__url)
            else:
                url = reverse(self.__url, kwargs={"path": self.__url_arg})
        except NoReverseMatch:
            url = self.__url
        return url


class AppCategory(Enum):
    Web = "web"
    App = "app"
    Map = "map"

    def label(self):
        return {
            AppCategory.Web: "<b>W</b>ebsites",
            AppCategory.App: "<b>A</b>pplications",
            AppCategory.Map: "<b>M</b>aps",
        }.get(self)

    def goto(self):
        return {
            AppCategory.Web: "Zur Seite",
            AppCategory.App: "Zum Tool",
            AppCategory.Map: "Zur Karte",
        }.get(self)


class AppIcon(Enum):
    Map = "img/icons_custom/Icon_map_w.png"
