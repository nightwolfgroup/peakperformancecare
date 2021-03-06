# Generated by Django 3.1.3 on 2020-11-18 22:44

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.contrib.routable_page.models
import wagtail.core.blocks
import wagtail.core.fields
import wagtailmetadata.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailcore', '0059_apply_collection_ordering'),
        ('wagtailimages', '0022_uploadedimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, help_text='A slug URL to identify posts by this category', max_length=255, populate_from='name', unique=True, verbose_name='Slug URL')),
            ],
            options={
                'verbose_name': 'Blog Category',
                'verbose_name_plural': 'Blog Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='BlogPageTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('content', wagtail.core.fields.StreamField([('content_block', wagtail.core.blocks.RichTextBlock(label='Content Block')), ('podcast', wagtail.core.blocks.StructBlock([])), ('podcast_episode', wagtail.core.blocks.StructBlock([('embed_code', wagtail.core.blocks.RawHTMLBlock(help_text='Place the entire embed code from Buzzsprout here', required=True))])), ('button', wagtail.core.blocks.StructBlock([('button', wagtail.core.blocks.StructBlock([('button_color', wagtail.core.blocks.ChoiceBlock(choices=[('Primary', (('btn-primary', 'Primary Solid'), ('btn-translucent-primary', 'Primary Translucent'), ('btn-outline-primary', 'Primary Outline'))), ('Secondary', (('btn-secondary', 'Secondary Solid'), ('btn-translucent-secondary', 'Secondary Translucent'), ('btn-outline-secondary', 'Secondary Outline'))), ('Success', (('btn-success', 'Success Solid'), ('btn-translucent-success', 'Success Translucent'), ('btn-outline-success', 'Success Outline'))), ('Danger', (('btn-danger', 'Danger Solid'), ('btn-translucent-danger', 'Danger Translucent'), ('btn-outline-danger', 'Danger Outline'))), ('Warning', (('btn-warning', 'Warning Solid'), ('btn-translucent-warning', 'Warning Translucent'), ('btn-outline-warning', 'Warning Outline'))), ('Info', (('btn-info', 'Info Solid'), ('btn-translucent-info', 'Info Translucent'), ('btn-outline-danger', 'Info Outline'))), ('Light', (('btn-light', 'Light Solid'), ('btn-translucent-light', 'Light Translucent'), ('btn-outline-light', 'Light Outline'))), ('Dark', (('btn-dark', 'Dark Solid'), ('btn-translucent-dark', 'Dark Translucent'), ('btn-outline-dark', 'Dark Outline')))])), ('button_text', wagtail.core.blocks.CharBlock(label='Button/Link Text', max_length=50)), ('internal_page', wagtail.core.blocks.PageChooserBlock(help_text='Point the link to an internal page.', label='Internal Page Link', required=False)), ('external_link', wagtail.core.blocks.URLBlock(help_text='Point the link to an external page.', label='External Page Link', required=False)), ('new_tab', wagtail.core.blocks.BooleanBlock(help_text='Check if you would like the link to open in a new tab when clicked.', label='Open Link In New Tab?', required=False))], required=True))])), ('blockquote', wagtail.core.blocks.StructBlock([('block_title', wagtail.core.blocks.CharBlock(help_text='Optional title to display above the blockquote', max_length=200, required=False)), ('quote', wagtail.core.blocks.RichTextBlock(required=True)), ('attribution', wagtail.core.blocks.CharBlock(max_length=500, required=True))]))])),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blog_post', to=settings.AUTH_USER_MODEL)),
                ('categories', modelcluster.fields.ParentalManyToManyField(blank=True, related_name='blog_post', to='blog.BlogCategory')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='wagtailimages.image', verbose_name='Cover Image')),
                ('search_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Search image')),
                ('tags', modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='blog.BlogPageTag', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Blog Post',
            },
            bases=(wagtailmetadata.models.MetadataMixin, 'wagtailcore.page', models.Model),
        ),
        migrations.AddField(
            model_name='blogpagetag',
            name='content_object',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_tags', to='blog.blogpost'),
        ),
        migrations.AddField(
            model_name='blogpagetag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_blogpagetag_items', to='taggit.tag'),
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('search_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Search image')),
            ],
            options={
                'verbose_name': 'Blog Home Page',
            },
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, wagtailmetadata.models.MetadataMixin, 'wagtailcore.page', models.Model),
        ),
    ]
