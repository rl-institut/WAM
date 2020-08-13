from enum import Enum
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


class AppInfo:
    """App infos are used on WAM landing page"""

    def __init__(
        self,
        category: str,
        name: str,
        url: str,
        closed: bool = False,
        icon: str = None,
        url_arg: str = None,
    ):
        """

        Parameters
        ----------
        category:
            Must be one of available app categories (AppCategory).
            App is placed in corresponding category section.
        name:
            Is displayed on landing page
        url: Either namespace url to django app, or fix url (to extern page)
        closed:
            If closed is active, a lock symbol is shown.
            (Access restrictions have to be set up by the app itself)
        icon: Icon to be shown on landing page
        url_arg: Optional path argument to (namespace) url - relict? unused?
        """
        self.category = category
        self.name = name
        self.__url = url
        self.closed = closed
        self.icon = icon
        self.__url_arg = url_arg

    @property
    def url(self):
        """
        Returns app url for landing page

        First reverse namespace url is tried (with url args if given), if this fails,
        url will be returned "as is".
        """
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
