# Generated by Django 2.2.5 on 2019-09-06 03:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0004_auto_20190905_0408'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='pid',
            field=models.ForeignKey(blank=True, help_text='对于非菜单权限需要选择一个可以成为菜单的权限，用户做默认展开菜单', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parents', to='rbac.Permission', verbose_name='关联所有权限'),
        ),
    ]
