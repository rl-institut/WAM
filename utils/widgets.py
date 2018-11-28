
from markdown import markdown
from itertools import count
from django.utils.safestring import mark_safe
from django.forms.renderers import get_default_renderer


class InfoButton(object):
    """
    Clickable icon "?" which opens reveal window showing info text

    Displays circled question mark. Hovering question mark will show tooltip,
    clicking on will open "reveal" window showing info text
    (markdown supported).
    """

    template_name = 'widgets/help_button.html'
    counter = count()

    def __init__(self, text, tooltip, is_markdown=False):
        """

        Parameters
        ----------
        text (str): Info text will appear in window. If text is written in
            markdown, parameter `is_markdown` must be set to True.
        tooltip (str): Text shown when hovering question mark icon
        is_markdown (bool): If set, text will be rendered as markdown into html
        """
        self.id = next(self.counter)
        self.text = markdown(text) if is_markdown else text
        self.tooltip = tooltip

    def __str__(self):
        return self.render()

    def get_context(self):
        return {
            'info_id': f'info_{self.id}',
            'text': self.text,
            'tooltip': self.tooltip
        }

    def render(self):
        """Render the widget as an HTML string."""
        context = self.get_context()
        return self._render(self.template_name, context)

    @staticmethod
    def _render(template_name, context):
        renderer = get_default_renderer()
        return mark_safe(renderer.render(template_name, context))
