from django.db import models

from .user import User
from ..libraries import utils


class Car(models.Model):
    color = utils.color
    carNum = models.CharField('车牌号', max_length=10)
    carColor = models.IntegerField('车身颜色', choices=color)
    carPrice = models.DecimalField('车辆价格(万元)', max_digits=10, decimal_places=2, default=0.0, blank=True, null=True)
    user = models.ManyToManyField(User)

    def __str__(self):
        return self.carNum
