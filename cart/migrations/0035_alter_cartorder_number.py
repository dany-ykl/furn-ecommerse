# Generated by Django 3.2.5 on 2021-10-23 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0034_alter_customer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='number',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
