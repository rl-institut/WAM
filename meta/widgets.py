from django.utils.safestring import mark_safe


class JsonWidget(object):
    def __init__(self, json):
        self.json = json

    def __convert_to_html(self, data, level=0):
        html = ''
        if isinstance(data, dict):
            html += f'<div style="margin-left: {level*2}rem;' \
                    f'margin-bottom: 0.75rem;' \
                    f'padding-left: 0.5rem;' \
                    f'border-left: 1px dotted #002E4F;">'\
                if level > 0 else '<div>'
            for key, value in data.items():
                html += f'<b>{key}:</b> {self.__convert_to_html(value, level+1)}'
            html += '</div>'
        elif isinstance(data, list):
            html += f'<div style="margin-left: {level*2}rem;">'
            for item in data:
                html += f'{self.__convert_to_html(item, level+1)}'
            html += '</div>'
        else:
            html += f'{data}<br>'
        return html

    def render(self):
        header = ''
        if self.json["title"] != "":
            header += f'<p class="lead">{self.json["title"]}</p>'
        if self.json["description"] != "":
            header += f'<p>{self.json["description"]}</p>'
        return mark_safe(header + self.__convert_to_html(data=self.json))
