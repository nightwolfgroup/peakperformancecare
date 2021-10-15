# Generated by Django 3.1.3 on 2020-11-19 20:39

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0006_auto_20201119_1222'),
    ]

    operations = [
        migrations.RenameField(
            model_name='videopasswordpage',
            old_name='tags',
            new_name='categories',
        ),
        migrations.AlterField(
            model_name='videotag',
            name='content_object',
            field=modelcluster.fields.ParentalKey(help_text='Comma-separated list of categories.', on_delete=django.db.models.deletion.CASCADE, related_name='video_tags', to='education.videopasswordpage'),
        ),
    ]