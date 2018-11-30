
from django.db import models


class Assumption(models.Model):
    """Defines an assumption for references.

    A source must be assigned to exactly one :class:`Source` defined in `source`.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    value = models.CharField(max_length=64)
    value_type = models.CharField(max_length=32)

    app_name = models.CharField(max_length=255)

    source = models.ForeignKey('Source', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Source(models.Model):
    """Defines a source in references, e.g. a book, thesis or dataset

    A source must be assigned to exactly one :class:`SourceCategory`  defined in `category`.
    """
    author = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField()
    year = models.IntegerField()
    license = models.CharField(max_length=255)

    app_name = models.CharField(max_length=255)

    category = models.ForeignKey('SourceCategory', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.author


class SourceCategory(models.Model):
    """Defines a source category in references, e.g. emissions.

    A category subsumes one or multiple sources, see :class:`Source`.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
