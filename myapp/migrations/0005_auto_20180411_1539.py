# Generated by Django 2.0.3 on 2018-04-11 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20180411_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='carPrice',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True, verbose_name='车辆价格'),
        ),
    ]