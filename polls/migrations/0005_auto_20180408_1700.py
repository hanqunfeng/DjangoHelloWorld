# Generated by Django 2.0.3 on 2018-04-08 09:00

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_question_uploadfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='uploadfile',
            field=models.FileField(default='', storage=django.core.files.storage.FileSystemStorage(base_url='http://localhost/files/', location='/Users/hanqunfeng/python_workspace/FILE/'), upload_to='file'),
        ),
    ]
