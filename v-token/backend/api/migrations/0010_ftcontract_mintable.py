# Generated by Django 3.2.8 on 2021-11-19 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20211027_0132'),
    ]

    operations = [
        migrations.AddField(
            model_name='ftcontract',
            name='mintable',
            field=models.BooleanField(default=False),
        ),
    ]