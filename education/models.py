from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import StreamFieldPanel, TabbedInterface, ObjectList, FieldPanel, PageChooserPanel, \
    MultiFieldPanel, InlinePanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail_color_panel.edit_handlers import NativeColorPanel
from wagtail_color_panel.fields import ColorField
from wagtailmenus.models import MenuPageMixin
from wagtailmenus.panels import menupage_panel
from wagtailmetadata.models import MetadataPageMixin

from blocks.blocks import IconCardsBlock, CTACircles, VideoShowcaseBlock, PodcastPlayerBlock
from blocks.choices import OPACITY_CHOICES


# Education Home Page ------------------------------------------------------------------------------------------------->
class Education(MetadataPageMixin, MenuPageMixin, Page):
    template = 'education/education-home.html'
    max_count = 1
    parent_page_types = ['core.HomePage', 'core.LinkPage']
    subpage_types = ['education.EducationPage', 'education.FAQPage', 'core.LinkPage']
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
        ('cards', IconCardsBlock()),
        ('cta', CTACircles())
    ])
    title_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('title_image'),
            NativeColorPanel('overlay_color'),
            FieldPanel('overlay_opacity'),
        ], heading='Title Image'),
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
        verbose_name = 'Education Home Page'


# Education Content Page ---------------------------------------------------------------------------------------------->
class EducationPage(MetadataPageMixin, Page):
    template = 'education/education.html'
    parent_page_types = ['education.Education']
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
    content = StreamField([
        ('videos', VideoShowcaseBlock()),
        ('cta', CTACircles()),
        ('podcast', PodcastPlayerBlock())
    ])
    title_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('title_image'),
            NativeColorPanel('overlay_color'),
            FieldPanel('overlay_opacity'),
        ], heading='Title Image'),
    ]
    content_panels = [
        StreamFieldPanel('content'),
    ]
    edit_handler = TabbedInterface([
        ObjectList(title_panels, heading='Title & Header'),
        ObjectList(content_panels, heading='Page Content'),
        ObjectList(MetadataPageMixin.promote_panels, heading='SEO/Menu'),
        ObjectList(Page.settings_panels, heading='Page Settings', classname='settings')
    ])

    class Meta:
        verbose_name = 'Education Page'


# FAQ Page ------------------------------------------------------------------------------------------------------------>
class FAQ(Orderable):
    page = ParentalKey('education.FAQPage', related_name='FAQs')
    question = models.CharField(blank=False, max_length=500)
    answer = models.TextField(blank=False)

    panels = [
        FieldPanel('question'),
        FieldPanel('answer')
    ]


class FAQPage(MetadataPageMixin, Page):
    template = 'education/faq-page.html'
    parent_page_types = ['education.Education']
    subpage_types = []
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            InlinePanel('FAQs', label='FAQ'),
        ], heading='Frequently Asked Questions', classname='collapsible'),
        MultiFieldPanel([
            InlinePanel('related_articles', label='Related Article'),
        ], heading='Related Articles')
    ]
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Page Content'),
        ObjectList(MetadataPageMixin.promote_panels, heading='SEO/Menu'),
        ObjectList(Page.settings_panels, heading='Page Settings', classname='settings')
    ])

    class Meta:
        verbose_name = 'FAQ Page'


# Related Articles Orderable ------------------------------------------------------------------------------------------>
class RelatedArticle(Orderable):
    page = ParentalKey('education.FAQPage', related_name='related_articles')
    related_article = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    panels = [
        PageChooserPanel('related_article')
    ]


# Password Protected Video List Page ---------------------------------------------------------------------------------->
class VideosPasswordPage(MetadataPageMixin, Page):
    template = 'videos/videos.html'
    parent_page_types = ['core.HomePage']
    sub_page_types = ['education.VideoPasswordPage']
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
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('title_image'),
            NativeColorPanel('overlay_color'),
            FieldPanel('overlay_opacity'),
        ], heading='Title Image'),
    ]
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Page Content'),
        ObjectList(MetadataPageMixin.promote_panels, heading='SEO/Menu'),
        ObjectList(Page.settings_panels, heading='Page Settings', classname='settings')
    ])

    class Meta:
        verbose_name = 'Password Video List Page'

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['tags'] = VideoPasswordPage.tags.all()
        context['all_videos'] = VideoPasswordPage.objects.all()
        return context


# Password Protected Video Page (Single) ------------------------------------------------------------------------------>
class VideoPasswordPage(MetadataPageMixin, Page):
    template = 'videos/video.html'
    password_required_template = 'videos/password-required.html'
    parent_page_types = ['education.VideosPasswordPage']
    sub_page_types = []
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
    video_thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        on_delete=models.PROTECT,
        related_name='+',
        verbose_name='Video Thumbnail'
    )
    youtube_link = models.URLField(
        blank=False,
        null=True,
        verbose_name='YouTube Link'
    )
    tags = ClusterTaggableManager(through='education.VideoTag', blank=True)
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('title_image'),
            NativeColorPanel('overlay_color'),
            FieldPanel('overlay_opacity'),
        ], heading='Title Image'),
        MultiFieldPanel([
            ImageChooserPanel('video_thumbnail'),
            FieldPanel('youtube_link'),
            FieldPanel('tags'),
        ], heading='Video')
    ]
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Page Content'),
        ObjectList(MetadataPageMixin.promote_panels, heading='SEO/Menu'),
        ObjectList(Page.settings_panels, heading='Page Settings', classname='settings')
    ])

    class Meta:
        verbose_name = 'Password Protected Video'


class VideoTag(TaggedItemBase):
    content_object = ParentalKey('VideoPasswordPage', related_name='video_tags')
