# Generated by Django 2.2.5 on 2019-09-11 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0007_auto_20190908_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='icon',
            field=models.CharField(max_length=32, verbose_name='图标'),
        ),
    ]
