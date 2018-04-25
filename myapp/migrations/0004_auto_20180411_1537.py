# Generated by Django 2.0.3 on 2018-04-11 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_car'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='carPrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='车辆价格'),
        ),
        migrations.AlterField(
            model_name='car',
            name='carColor',
            field=models.IntegerField(choices=[(1, 'red'), (2, 'black'), (3, 'blue')], verbose_name='车身颜色'),
        ),
        migrations.AlterField(
            model_name='car',
            name='carNum',
            field=models.CharField(max_length=10, verbose_name='车牌号'),
        ),
    ]