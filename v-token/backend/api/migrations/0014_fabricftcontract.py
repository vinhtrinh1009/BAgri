# Generated by Django 3.2.8 on 2021-12-24 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_bridgesmartcontract'),
    ]

    operations = [
        migrations.CreateModel(
            name='FabricFTContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token_standard', models.CharField(choices=[('ERC-20', 'Erc 20'), ('ERC-777', 'Erc 777')], max_length=16)),
                ('token_name', models.CharField(max_length=64)),
                ('token_symbol', models.CharField(max_length=8)),
                ('token_icon', models.FileField(blank=True, null=True, upload_to='')),
                ('decimal', models.PositiveSmallIntegerField(default=18)),
                ('initial_supply', models.PositiveBigIntegerField(default=0)),
                ('user_id', models.CharField(max_length=64)),
                ('network_id', models.CharField(blank=True, max_length=64, null=True)),
                ('chaincode_id', models.CharField(blank=True, max_length=64, null=True)),
            ],
        ),
    ]
