# Generated by Django 3.2.5 on 2021-09-08 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_slug'),
        ('cart', '0026_alter_cartorder_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='related_order', to='shop.Product'),
        ),
    ]
