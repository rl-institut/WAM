
from django.db import models
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
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Source(models.Model):
    """Defines a source in references, e.g. a book, thesis or dataset

    A source must be assigned to exactly one :class:`Category`
    defined in `category`.
    """
    author = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField()
    year = models.IntegerField()
    license = models.CharField(max_length=255)
    meta_data = JSONField(null=True)

    app_name = models.CharField(max_length=255)

    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.author

    def render_json(self):
        return JsonWidget(self.meta_data).render()

    def render_url(self):
        try:
            return self.meta_data['sources'][0]['url']
        except (KeyError, IndexError):
            return None


class Category(models.Model):
    """Defines a category in references, e.g. emissions.

    A category subsumes one or multiple sources, see :class:`Source`.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
