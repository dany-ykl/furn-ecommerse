# Generated by Django 3.2.5 on 2021-08-21 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_alter_cartorder_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='order',
            field=models.CharField(max_length=100),
        ),
    ]
