import jmespath

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

    source = models.ForeignKey("Source", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Source(models.Model):
    """Defines a source in references, e.g. a book, thesis or dataset

    A source must be assigned to exactly one :class:`Category`
    defined in `category`.
    """

    meta_data = JSONField(null=True)

    app_name = models.CharField(max_length=255)

    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    def json(self):
        return JsonWidget(self.meta_data).render()

    def infos(self):
        infos = jmespath.search(
            "{"
            "url: identifier, "
            "title: title, "
            "description: description, "
            "licenses: licenses[*].name"
            "}",
            self.meta_data,
        )
        if infos.get("url") is not None:
            if infos.get("url") == "":
                infos.pop("url")
        else:
            infos.pop("url")
        return infos


class Category(models.Model):
    """Defines a category in references, e.g. emissions.

    A category subsumes one or multiple sources, see :class:`Source`.
    """

    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
