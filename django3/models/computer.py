from django.db import models


class Computer(models.Model):
    name = models.CharField('电脑品牌', max_length=50, db_column='name')
    cpu_num = models.IntegerField('cpu核数', default=0)
    memory = models.IntegerField('内存(G)', default=8)

    class Meta:
        db_table = "django3_computer"
        app_label = "django3"

    def __str__(self):
        return self.name
