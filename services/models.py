from django.db import models
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel, StreamFieldPanel, TabbedInterface, ObjectList
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail_color_panel.edit_handlers import NativeColorPanel
from wagtail_color_panel.fields import ColorField
from wagtailmenus.models import MenuPageMixin
from wagtailmenus.panels import menupage_panel
from wagtailmetadata.models import MetadataPageMixin
from blocks.blocks import CTACircles, PersonalMessageBlock, VideoSplitBlock, FreeReportBlock
from blocks.choices import OPACITY_CHOICES


# Physical Therapy Services Home Page --------------------------------------------------------------------------------->
class PhysicalTherapy(MetadataPageMixin, MenuPageMixin, Page):
    template = 'services/services.html'
    max_count = 1
    parent_page_types = ['core.HomePage']
    subpage_types = ['services.PTService']

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

    content = StreamField([
        ('cta', CTACircles())
    ])

    title_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('title_image'),
            NativeColorPanel('overlay_color'),
            FieldPanel('overlay_opacity')
        ], heading='Title Image')
    ]
    content_panels = [
        StreamFieldPanel('content')
    ]
    settings_panels = Page.settings_panels + [
        menupage_panel
    ]
    edit_handler = TabbedInterface([
        ObjectList(title_panels, heading='Title & Header'),
        ObjectList(content_panels, heading='Page Content'),
        ObjectList(MetadataPageMixin.promote_panels, heading='SEO/Menu'),
        ObjectList(settings_panels, heading='Page Settings', classname='settings')
    ])

    class Meta:
        verbose_name = 'Physical Therapy Services Home Page'

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        services = PTService.objects.live().public()
        context['services'] = services
        return context


# Physical Therapy Service Page --------------------------------------------------------------------------------------->
class PTService(MetadataPageMixin, Page):
    template = 'services/service.html'
    parent_page_types = ['services.PhysicalTherapy']
    subpage_types = []
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
    form_title = models.CharField(
        blank=False,
        null=True,
        max_length=255,
        default='Fill Out This Form to Receive the FREE Guide on How to Quickly Eliminate Your ____ Pain!'
    )
    form = models.TextField(
        blank=False,
        null=True,
        verbose_name='Infusionsoft Form'
    )
    service_icon = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        on_delete=models.PROTECT,
        related_name='+',
        verbose_name='Service Icon',
        help_text='Icon used for service list page.'
    )
    service_description = RichTextField(
        blank=True,
        null=True,
        verbose_name='Service Description'
    )
    content = StreamField([
        ('free_report', FreeReportBlock()),
        ('cta', CTACircles()),
        ('message', PersonalMessageBlock()),
        ('video_split', VideoSplitBlock()),
    ])

    title_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('title_image'),
            NativeColorPanel('overlay_color'),
            FieldPanel('overlay_opacity')
        ], heading='Title Image')
    ]

    content_panels = [
        StreamFieldPanel('content')
    ]

    form_panels = [
        MultiFieldPanel([
            FieldPanel('form_title'),
            FieldPanel('form')
        ], heading='Infusionsoft Form')
    ]

    service_panels = [
        ImageChooserPanel('service_icon'),
        FieldPanel('service_description')
    ]

    edit_handler = TabbedInterface([
        ObjectList(title_panels, heading='Title & Header'),
        ObjectList(content_panels, heading='Page Content'),
        ObjectList(form_panels, heading='Opt-In Form'),
        ObjectList(service_panels, heading='Service Info'),
        ObjectList(MetadataPageMixin.promote_panels, heading='SEO/Menu'),
        ObjectList(Page.settings_panels, heading='Page Settings', classname='settings')
    ])

    class Meta:
        verbose_name = 'Physical Therapy Service'


# Wellness Services Home Page ----------------------------------------------------------------------------------------->
class Wellness(MetadataPageMixin, MenuPageMixin, Page):
    template = 'services/services.html'
    max_count = 1
    parent_page_types = ['core.HomePage']
    subpage_types = ['services.WellnessService']

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

    content = StreamField([
        ('cta', CTACircles())
    ])

    title_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('title_image'),
            NativeColorPanel('overlay_color'),
            FieldPanel('overlay_opacity')
        ], heading='Title Image')
    ]
    content_panels = [
        StreamFieldPanel('content')
    ]
    settings_panels = Page.settings_panels + [
        menupage_panel
    ]
    edit_handler = TabbedInterface([
        ObjectList(title_panels, heading='Title & Header'),
        ObjectList(content_panels, heading='Page Content'),
        ObjectList(MetadataPageMixin.promote_panels, heading='SEO/Menu'),
        ObjectList(settings_panels, heading='Page Settings', classname='settings')
    ])

    class Meta:
        verbose_name = 'Wellness Services Home Page'

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        services = WellnessService.objects.live().public()
        context['services'] = services
        return context


# Wellness Service Page ----------------------------------------------------------------------------------------------->
class WellnessService(MetadataPageMixin, Page):
    template = 'services/service.html'
    parent_page_types = ['services.Wellness']
    subpage_types = []
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
    form_title = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        default='Fill Out This Form to Receive the FREE Guide on How to Quickly Eliminate Your ____ Pain!'
    )
    form = models.TextField(
        blank=True,
        null=True,
        verbose_name='Infusionsoft Form'
    )
    service_icon = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        on_delete=models.PROTECT,
        related_name='+',
        verbose_name='Service Icon',
        help_text='Icon used for service list page.'
    )
    service_description = RichTextField(
        blank=True,
        null=True,
        verbose_name='Service Description'
    )
    content = StreamField([
        ('free_report', FreeReportBlock()),
        ('cta', CTACircles()),
        ('message', PersonalMessageBlock()),
        ('video_split', VideoSplitBlock()),
    ])

    title_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('title_image'),
            NativeColorPanel('overlay_color'),
            FieldPanel('overlay_opacity')
        ], heading='Title Image')
    ]

    content_panels = [
        StreamFieldPanel('content')
    ]

    form_panels = [
        MultiFieldPanel([
            FieldPanel('form_title'),
            FieldPanel('form')
        ], heading='Infusionsoft Form')
    ]

    service_panels = [
        ImageChooserPanel('service_icon'),
        FieldPanel('service_description')
    ]

    edit_handler = TabbedInterface([
        ObjectList(title_panels, heading='Title & Header'),
        ObjectList(content_panels, heading='Page Content'),
        ObjectList(form_panels, heading='Opt-In Form'),
        ObjectList(service_panels, heading='Service Info'),
        ObjectList(MetadataPageMixin.promote_panels, heading='SEO/Menu'),
        ObjectList(Page.settings_panels, heading='Page Settings', classname='settings')
    ])

    class Meta:
        verbose_name = 'Wellness Service'
