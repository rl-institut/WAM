
from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.postgres.fields import JSONField

from meta.widgets import JsonWidget


class Assumption(models.Model):
    """Defines an assumption for references.

    A source must be assigned to exactly one :class:`Source` defined in
    `source`.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    value = models.CharField(max_length=64)
    unit = models.CharField(max_length=32)

    app_name = models.CharField(max_length=255)

    source = models.ForeignKey('Source', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Source(models.Model):
    """Defines a source in references, e.g. a book, thesis or dataset

    A source must be assigned to exactly one :class:`SourceCategory`
    defined in `category`.
    """
    author = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField()
    year = models.IntegerField()
    license = models.CharField(max_length=255)
    meta_data = JSONField(null=True)

    app_name = models.CharField(max_length=255)

    category = models.ForeignKey('SourceCategory', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.author

    @property
    def html(self):
        if self.meta_data is None:
            html = (
                f'<a href="{self.url}" target="_blank">{self.author}</a>:' 
                f'{self.description}, {self.year}, {self.license}'
            )
        else:
            html = ''

            try:
                author = ', '.join(
                    contributor['name']
                    for contributor in self.meta_data['contributors']
                )
            except KeyError:
                author = ''

            try:
                url = self.meta_data['sources'][0]['url']
                html += f'<a href="{url}" target="_blank">{author}</a>'
            except (KeyError, IndexError):
                html += f'{author}'

            try:
                _license = self.meta_data['licence']['id']
                html += f', {_license}'
            except KeyError:
                pass

            # Add rest of json within modal:
            html += (
                f'<span class="has-tip--no-border">'
                f'<i data-open="meta_data_{self.id}" class ="icon ion-information-circled icon--small info-box" title="Hier klicken für mehr Informationen zum {{option.label}}"></i>'
                '</span>'
                f'<div class="reveal" id="meta_data_{self.id}" data-reveal>'
                f'{JsonWidget(self.meta_data).render()}'
                '</div'
            )
        return mark_safe(html)


class SourceCategory(models.Model):
    """Defines a source category in references, e.g. emissions.

    A category subsumes one or multiple sources, see :class:`Source`.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
