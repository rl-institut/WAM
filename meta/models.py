
from django.db import models


class Assumption(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    value = models.CharField(max_length=64)
    value_type = models.CharField(max_length=32)

    app_name = models.CharField(max_length=255)

    source = models.ForeignKey('Source', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Source(models.Model):
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
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
