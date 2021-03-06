import os
from abc import ABC
from typing import List, Tuple, Optional
from itertools import count
from collections import ChainMap, namedtuple
import pandas
from markdown import markdown

from django.utils.safestring import mark_safe
from django.forms.renderers import get_default_renderer

from wam.settings import BASE_DIR

# import markdownx extensions from settings if available
try:
    from wam.settings import MARKDOWNX_MARKDOWN_EXTENSIONS
except ImportError:
    MARKDOWNX_MARKDOWN_EXTENSIONS = []


class CustomWidget(ABC):
    template_name: str = None

    def __str__(self):
        return self.render()

    def get_context(self):  # pylint: disable=no-self-use
        return {}

    def render(self):
        """Render the widget as an HTML string."""
        context = self.get_context()
        return self._render(self.template_name, context)

    @staticmethod
    def _render(template_name, context):
        renderer = get_default_renderer()
        return mark_safe(renderer.render(template_name, context))


class InfoButton(CustomWidget):
    """
    Clickable icon which opens reveal window showing info text

    Displays icon. Hovering show tooltip, clicking on will open "reveal" window
    showing info text (markdown supported).
    """

    template_name = "widgets/info_button.html"
    counter = count()

    def __init__(
        self,
        text: str = "",
        tooltip: str = "",
        is_markdown: bool = False,
        ionicon_type: str = "ion-information-circled",
        ionicon_size: str = "small",
        ionicon_color: str = None,
        info_id: str = None,
    ):
        """

        Parameters
        ----------
        text : str
            Info text will appear in window. If text is written in markdown,
            parameter `is_markdown` must be set to True.
        tooltip : str
            Text shown when hovering question mark icon
        is_markdown : bool
            If set, text will be rendered as markdown into html
        ionicon_type : str
            Defines type of ionicon, for v2 refer to https://ionicons.com/v2/
        ionicon_size : str
            Sets size of icon, possible values: small, medium, large, xlarge,
            xxlarge
        ionicon_color : str
            Sets color of icon in hex color code, e.g. '#ff0000'
        info_id : str
            Optional. If provided, the reveal div id will be set to this value,
            prepended by "info_". By default, a counter is used which results
            in ids "info_0", "info_1" etc.
        """
        self.text = (
            markdown(text, extensions=MARKDOWNX_MARKDOWN_EXTENSIONS)
            if is_markdown
            else text
        )
        self.tooltip = tooltip
        self.ionicon_type = ionicon_type
        self.ionicon_size = ionicon_size
        self.ionicon_color = ionicon_color

        if info_id is not None and isinstance(info_id, str):
            self.id = info_id
        else:
            self.id = next(self.counter)

    def get_context(self):
        return {
            "info_id": f"info_{self.id}",
            "text": self.text,
            "tooltip": self.tooltip,
            "ionicon_type": self.ionicon_type,
            "ionicon_size": self.ionicon_size,
            "ionicon_color": self.ionicon_color,
        }


class Wizard(CustomWidget):
    """
    Step-Wizard showing active, current and coming steps

    Active steps are hrefs, current step is circled, coming steps are inactive.
    Optionally, screen reader text for current step can be given.
    """

    template_name = "widgets/wizard.html"

    def __init__(
        self,
        urls: List[Optional[Tuple[str, str]]],
        current: int,
        screen_reader_for_current: str = None,
    ):
        """

        Parameters
        ----------
        urls :
            Clicking on steps can redirect to given urls. If steps without url
            shall be shown enter "None".
        current : int
            Circles current step
        screen_reader_for_current : str
            Screen reader text for curretn step supported
        """
        self.urls = urls
        self.current = current
        self.screen_reader = screen_reader_for_current

    def get_context(self):
        return {
            "urls": self.urls,
            "current": self.current,
            "screen_reader": self.screen_reader,
        }


class CSVWidget:
    """Reads in CSV-file and renders it as table"""

    def __init__(
        self, filename, caption, csv_kwargs=None, html_kwargs=None, links=None
    ):
        """
        Parameters
        ----------
        filename: str
            Filename is joined with basic wam-path. Thus, if file "nems.csv"
            in folder "texts" from app "stemp" shall be loaded, filename has to
            be given as 'stemp/texts/names.csv'
        caption: str
            Caption for table
        csv_kwargs: dict
            csv_kwargs are passed to `pandas.read_csv`
        html_kwargs: dict
            html_kwargs are passed to `pandas.style`
        links: list-of-str
            List of columns which shall be wrapped in html <a>-tag
        """
        self.caption = caption
        self.html_kwargs = {} if html_kwargs is None else html_kwargs
        links = [] if links is None else links

        filename = os.path.join(BASE_DIR, filename)
        csv_kwargs = {} if csv_kwargs is None else csv_kwargs
        self.data = pandas.read_csv(filename, **csv_kwargs)
        for link in links:
            self.data[link] = self.data[link].apply(lambda x: f'<a href="{x}">{x}</a>')
        self.data.fillna("-", inplace=True)

    def __str__(self):
        style = self.data.style
        style.set_caption(self.caption)
        return mark_safe(style.render(**self.html_kwargs))


class OrbitWidget(CustomWidget):
    OrbitItem = namedtuple("OrbitItem", ["name", "description", "class_"])
    OrbitItem.__new__.__defaults__ = (None,)

    template_name = "widgets/orbit.html"
    default_labels = {"next": "Nächster", "previous": "Vorheriger"}

    def __init__(
        self,
        caption: str,
        orbits: List[OrbitItem],
        labels: dict = None,
        orbit_class="orbit",
    ):
        if labels is None:
            labels = {}
        self.labels = ChainMap(self.default_labels, labels)
        self.caption = caption
        self.orbits = orbits
        self.orbit_class = orbit_class

    def get_context(self):
        return {
            "caption": self.caption,
            "labels": self.labels,
            "orbits": self.orbits,
            "orbit_class": self.orbit_class,
        }
