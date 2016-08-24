from django.db import models


class Organization(models.Model):
    name = models.CharField(verbose_name="NAME", max_length=100)


class Person(models.Model):
    name = models.CharField(verbose_name="full name", max_length=100)
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.CASCADE)
    married = models.BooleanField(verbose_name="married", default=False)
