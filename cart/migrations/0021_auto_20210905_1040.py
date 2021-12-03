# Generated by Django 3.2.5 on 2021-09-05 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0020_auto_20210824_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email_or_session',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='session_id',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
