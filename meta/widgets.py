
from django.utils.safestring import mark_safe


class JsonWidget(object):
    def __init__(self, json):
        self.json = json

    def __convert_to_html(self, data):
        html = ''
        if isinstance(data, dict):
            for key, value in data.items():
                html += f'<b>{key}:</b> {self.__convert_to_html(value)}'
        elif isinstance(data, list):
            html += '<ul>'
            for item in data:
                html += f'<li>{self.__convert_to_html(item)}</li>'
            html += '</ul>'
        else:
            html += f'{data}<br>'
        return html

    def render(self):
        return mark_safe(self.__convert_to_html(self.json))
