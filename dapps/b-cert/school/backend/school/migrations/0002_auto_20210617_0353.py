# Generated by Django 2.2.24 on 2021-06-17 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='private_key',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='public_key',
            field=models.CharField(max_length=256, null=True),
        ),
    ]