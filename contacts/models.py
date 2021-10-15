from django.db import models
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel, TabbedInterface, ObjectList
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail_color_panel.edit_handlers import NativeColorPanel
from wagtail_color_panel.fields import ColorField
from wagtailmenus.models import MenuPageMixin
from wagtailmenus.panels import menupage_panel
from wagtailmetadata.models import MetadataPageMixin

from blocks.choices import OPACITY_CHOICES


# Contact Page -------------------------------------------------------------------------------------------------------->
class ContactPage(MetadataPageMixin, MenuPageMixin, Page):
    template = 'contacts/contact.html'
    max_count = 4
    parent_page_types = ['core.HomePage', 'contacts.ContactPage']
    subpage_types = ['contacts.ContactPage']
    title_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        on_delete=models.PROTECT,
        related_name='+',
        verbose_name='Image'
    )
    overlay_color = ColorField(
        default='#000000',
        verbose_name='Overlay Color'
    )
    overlay_opacity = models.CharField(
        choices=OPACITY_CHOICES,
        max_length=4,
        default='.7',
        blank=False,
        null=False,
        verbose_name='Overlay Opacity'
    )
    form = models.TextField(
        max_length=2000,
        verbose_name='Infusionsoft Embed Code',
        blank=False,
        null=True,
        help_text='Place the entire Infusionsoft JavaScript snippet for the form here.'
    )
    map_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        on_delete=models.PROTECT,
        related_name='+',
        verbose_name='Map Image'
    )
    map_link = models.CharField(
        blank=False,
        null=True,
        max_length=1000,
        verbose_name='Google Map Embed URL',
        default='https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3145.0021611401385!2d-120.3411954482222!3d37.97'
                '7078879623534!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x8090c5d17033cac3%3A0x74f095a97c40b69'
                '4!2sPeak%20Performance%20Care!5e0!3m2!1sen!2sus!4v1605503238589!5m2!1sen!2sus'
    )
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('title_image'),
            NativeColorPanel('overlay_color'),
            FieldPanel('overlay_opacity'),
        ], heading='Title Image'),
        FieldPanel('form', classname='full'),
        MultiFieldPanel([
            ImageChooserPanel('map_image'),
            FieldPanel('map_link'),
        ], heading='Map'),
    ]
    settings_panels = Page.settings_panels + [
        menupage_panel
    ]
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Page Content'),
        ObjectList(MetadataPageMixin.promote_panels, heading='SEO/Menu'),
        ObjectList(settings_panels, heading='Page Settings', classname='settings')
    ])

    class Meta:
        verbose_name = 'Contact Page'
