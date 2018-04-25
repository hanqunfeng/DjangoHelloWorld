from django.db import models

from .user import User


class IdentityCard(models.Model):
    cardId = models.CharField('身份证号', max_length=20, blank=True, null=True)
    address = models.CharField('地址', max_length=20, blank=True, null=True)
    issuing_organ = models.CharField('发证机关', max_length=20, blank=True, null=True)
    validity_date = models.DateField('有效期截止', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        db_table = "sys_user_idcard"

    def __str__(self):
        return self.cardId
