from django.db import models

from .person import Person


class User(Person):
    phone = models.CharField('手机号码', max_length=20, blank=True, null=True)
    email = models.EmailField('邮箱', blank=True, null=True)

    class Meta(Person.Meta):
        db_table = "sys_user"

    def __str__(self):
        return self.name
