# Generated by Django 3.2.5 on 2021-08-21 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0015_remove_cartorder_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartorder',
            name='tess',
        ),
    ]
