# Generated by Django 3.1.4 on 2020-12-11 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_server', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filestorage',
            name='file_path',
            field=models.FilePathField(path='/home/evgeny', verbose_name='Path'),
        ),
    ]
