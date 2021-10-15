# Generated by Django 3.1.3 on 2020-11-19 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_remove_wellnessservice_service_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wellnessservice',
            name='form',
            field=models.TextField(blank=True, null=True, verbose_name='Infusionsoft Form'),
        ),
        migrations.AlterField(
            model_name='wellnessservice',
            name='form_title',
            field=models.CharField(blank=True, default='Fill Out This Form to Receive the FREE Guide on How to Quickly Eliminate Your ____ Pain!', max_length=255, null=True),
        ),
    ]
