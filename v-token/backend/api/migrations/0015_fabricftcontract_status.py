# Generated by Django 3.2.8 on 2021-12-28 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_fabricftcontract'),
    ]

    operations = [
        migrations.AddField(
            model_name='fabricftcontract',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Fail', 'Fail'), ('Succes', 'Success')], default='Pending', max_length=16),
        ),
    ]
