from django.db import models


class Person(models.Model):
    name = models.CharField('姓名', max_length=30)
    birth_day = models.DateField('出生日期', blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ['name']
