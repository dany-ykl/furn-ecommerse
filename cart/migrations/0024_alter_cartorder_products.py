# Generated by Django 3.2.5 on 2021-09-08 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0023_cartorder_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='related_products', to='cart.OrderItem'),
        ),
    ]