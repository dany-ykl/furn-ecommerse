# Generated by Django 3.2.5 on 2021-08-22 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0016_remove_cartorder_tess'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.order'),
        ),
    ]
