# Generated by Django 3.2.5 on 2021-09-05 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0021_auto_20210905_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='total_products',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='delivery',
            field=models.CharField(choices=[('free', 'Pickup'), ('info', 'Delivery by mail'), ('info', 'Delivery by courier')], max_length=50),
        ),
    ]
