# Generated by Django 3.2.5 on 2021-08-24 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_slug'),
        ('cart', '0019_cartorder_final_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartorder',
            name='order',
        ),
        migrations.AddField(
            model_name='cartorder',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='related_products', to='shop.Product'),
        ),
    ]
