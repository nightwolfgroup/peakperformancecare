# Generated by Django 3.1.3 on 2020-11-19 04:00

from django.db import migrations, models
import django.db.models.deletion
import wagtail_color_panel.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0022_uploadedimage'),
        ('education', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videospasswordpage',
            name='hero',
        ),
        migrations.AddField(
            model_name='videospasswordpage',
            name='overlay_color',
            field=wagtail_color_panel.fields.ColorField(default='#000000', max_length=7, verbose_name='Overlay Color'),
        ),
        migrations.AddField(
            model_name='videospasswordpage',
            name='overlay_opacity',
            field=models.CharField(choices=[('0', '0%'), ('.1', '10%'), ('.2', '20%'), ('.3', '30%'), ('.4', '40%'), ('.5', '50%'), ('.6', '60%'), ('.7', '70%'), ('.8', '80%'), ('.9', '90%'), ('1', '100%')], default='.7', max_length=4, verbose_name='Overlay Opacity'),
        ),
        migrations.AddField(
            model_name='videospasswordpage',
            name='title_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtailimages.image', verbose_name='Image'),
        ),
    ]
