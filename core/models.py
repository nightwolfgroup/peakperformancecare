from django.db import models
from taggit.models import Tag as TaggitTag
from wagtail.admin.edit_handlers import StreamFieldPanel, TabbedInterface, ObjectList, MultiFieldPanel, FieldPanel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core.blocks import RichTextBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail_color_panel.edit_handlers import NativeColorPanel
from wagtail_color_panel.fields import ColorField
from wagtailmenus.models import AbstractLinkPage
from wagtailmetadata.models import MetadataPageMixin

from blocks.blocks import MainTitleBlock, BiographyBlock, TelehealthBlock, CTACards, CTACircles, CTAGuides, \
    TestimonialCards, PageTitleBlock, ServiceTitle, TeamBlock, PeopleWeHelpBlock, VideoSplitBlock, \
    VideoShowcaseBlock, PersonalMessageBlock, IconCardsBlock, PodcastPlayerBlock, PodcastEpisodeBlock, ModalFormBlock, \
    BlockquoteBlock
from blocks.choices import OPACITY_CHOICES


# Home Page ----------------------------------------------------------------------------------------------------------->
class HomePage(MetadataPageMixin, Page):
    template = 'core/index.html'
    max_count = 1
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
    heading = models.CharField(
        max_length=255,
        help_text='Main title text.',
        blank=False,
        null=True,
        default='We Help Active Adults Who Want To Get Back To The Activities They Love Without Medication & Surgery'
    )
    subheading = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text='Optional text to display below the title.',
        default="Get The Healthy Lifestyle You've Always Wanted!"
    )
    content = StreamField([
        ('biography', BiographyBlock()),
        ('telehealth', TelehealthBlock()),
        ('cta_cards', CTACards()),
        ('cta_circles', CTACircles()),
        ('cta_guides', CTAGuides()),
        ('testimonials', TestimonialCards()),
    ])
    title_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('title_image'),
            NativeColorPanel('overlay_color'),
            FieldPanel('overlay_opacity')
        ], heading='Title Image'),
        MultiFieldPanel([
            FieldPanel('heading', classname='full'),
            FieldPanel('subheading', classname='full')
        ], heading='Title Text')

    ]
    content_panels = [
        StreamFieldPanel('content')
    ]
    edit_handler = TabbedInterface([
        ObjectList(title_panels, heading='Title & Header'),
        ObjectList(content_panels, heading='Page Content'),
        ObjectList(MetadataPageMixin.promote_panels, heading='SEO/Menu'),
        ObjectList(Page.settings_panels, heading='Page Settings', classname='settings')
    ])

    class Meta:
        verbose_name = 'Home Page'


# Landing Page -------------------------------------------------------------------------------------------------------->
class LandingPage(MetadataPageMixin, Page):
    template = 'core/streamfield-page.html'
    hero = StreamField([
        ('title1', MainTitleBlock()),
        ('title2', PageTitleBlock()),
        ('title3', ServiceTitle()),
    ])
    content = StreamField([
        ('biography', BiographyBlock()),
        ('telehealth', TelehealthBlock()),
        ('team', TeamBlock()),
        ('people_we_help', PeopleWeHelpBlock()),
        ('video_split', VideoSplitBlock()),
        ('video_showcase', VideoShowcaseBlock()),
        ('personal_message', PersonalMessageBlock()),
        ('icon_cards', IconCardsBlock()),
        ('podcast_player', PodcastPlayerBlock()),
        ('podcast_episode', PodcastEpisodeBlock()),
        ('modal_form', ModalFormBlock()),
        ('cta_cards', CTACards()),
        ('cta_circles', CTACircles()),
        ('cta_guides', CTAGuides()),
        ('testimonial_cards', TestimonialCards()),
        ('rich_text', RichTextBlock()),
        ('blockquote', BlockquoteBlock())
    ])
    title_panels = Page.content_panels + [
        StreamFieldPanel('hero')
    ]
    content_panels = [
        StreamFieldPanel('content')
    ]
    edit_handler = TabbedInterface([
        ObjectList(title_panels, heading='Title & Header'),
        ObjectList(content_panels, heading='Page Content'),
        ObjectList(MetadataPageMixin.promote_panels, heading='SEO/Menu'),
        ObjectList(Page.settings_panels, heading='Page Settings', classname='settings')
    ])

    class Meta:
        verbose_name = 'Landing Page'


# Menu Link Pages ----------------------------------------------------------------------------------------------------->
class LinkPage(AbstractLinkPage):
    pass

    class Meta:
        verbose_name = 'Link Page'


# Business Settings --------------------------------------------------------------------------------------------------->
@register_setting(icon='fa-building-o')
class BusinessSettings(BaseSetting):
    # Business Contact Information
    name = models.CharField(
        max_length=255,
        blank=False,
        null=True,
        verbose_name='Name',
        default='Peak Performance Care Physical Therapy'
    )
    street_address = models.CharField(
        max_length=255,
        blank=False,
        null=True,
        verbose_name='Street',
        default='13949 Mono Way'
    )
    mailing_address = models.CharField(
        max_length=255,
        blank=False,
        null=True,
        verbose_name='Mailing',
        default='PO Box 4143'
    )
    city = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name='City',
        default='Sonora'
    )
    state = models.CharField(
        max_length=2,
        blank=False,
        null=False,
        verbose_name='State',
        default='CA'
    )
    zip = models.CharField(
        max_length=5,
        blank=False,
        null=False,
        verbose_name='Zip',
        default='95370'
    )
    phone = models.CharField(
        max_length=255,
        blank=False,
        null=True,
        verbose_name='Phone',
        default='(209) 532-1288'
    )
    fax = models.CharField(
        max_length=255,
        blank=False,
        null=True,
        verbose_name='Fax',
        default='(209) 533-5372'
    )
    email = models.EmailField(
        blank=False,
        null=True,
        verbose_name='Email',
        default='info@peakperformancecare.com'
    )

    # Business Hours
    sun_open = models.TimeField(
        blank=False,
        null=False,
        default='00:00:00',
        verbose_name='Open',
    )
    sun_close = models.TimeField(
        blank=False,
        null=False,
        default='00:00:00',
        verbose_name='Close',
    )
    mon_open = models.TimeField(
        blank=False,
        null=False,
        default='08:00:00',
        verbose_name='Open'
    )
    mon_close = models.TimeField(
        blank=False,
        null=False,
        default='16:30:00',
        verbose_name='Close'
    )
    tue_open = models.TimeField(
        blank=False,
        null=False,
        default='08:00:00',
        verbose_name='Open'
    )
    tue_close = models.TimeField(
        blank=False,
        null=False,
        default='16:30:00',
        verbose_name='Close'
    )
    wed_open = models.TimeField(
        blank=False,
        null=False,
        default='08:00:00',
        verbose_name='Open'
    )
    wed_close = models.TimeField(
        blank=False,
        null=False,
        default='16:30:00',
        verbose_name='Close'
    )
    thu_open = models.TimeField(
        blank=False,
        null=False,
        default='08:00:00',
        verbose_name='Open'
    )
    thu_close = models.TimeField(
        blank=False,
        null=False,
        default='16:30:00',
        verbose_name='Close'
    )
    fri_open = models.TimeField(
        blank=False,
        null=False,
        default='08:00:00',
        verbose_name='Open'
    )
    fri_close = models.TimeField(
        blank=False,
        null=False,
        default='16:30:00',
        verbose_name='Close'
    )
    sat_open = models.TimeField(
        blank=False,
        null=False,
        default='00:00:00',
        verbose_name='Open',
    )
    sat_close = models.TimeField(
        blank=False,
        null=False,
        editable=True,
        default='00:00:00',
        verbose_name='Close',
    )
    # Business Logo
    logo_light = models.ForeignKey(
        'wagtailimages.image',
        on_delete=models.PROTECT,
        verbose_name='Main (light)',
        null=True,
        related_name='logo_light'
    )
    logo_dark = models.ForeignKey(
        'wagtailimages.image',
        on_delete=models.PROTECT,
        verbose_name='Main (dark)',
        null=True,
        related_name='logo_dark'
    )
    logo_footer = models.ForeignKey(
        'wagtailimages.image',
        on_delete=models.PROTECT,
        verbose_name='Footer',
        null=True,
        related_name='logo_footer'
    )
    logo_footer_alt = models.ForeignKey(
        'wagtailimages.image',
        on_delete=models.PROTECT,
        verbose_name='Footer (alt)',
        null=True,
        related_name='logo_footer_alt'
    )
    logo_icon = models.ForeignKey(
        'wagtailimages.image',
        on_delete=models.PROTECT,
        verbose_name='Icon',
        null=True,
        related_name='logo_icon'
    )
    logo_icon_footer = models.ForeignKey(
        'wagtailimages.image',
        on_delete=models.PROTECT,
        verbose_name='Footer icon',
        null=True,
        related_name='logo_icon_footer'
    )
    # Social Media Accounts
    facebook = models.URLField(
        blank=True,
        null=True,
        help_text="Facebook URL",
        default='https://www.facebook.com/PeakPerformanceCare/'
    )
    twitter = models.URLField(
        blank=True,
        null=True,
        help_text="Twitter URL",
        default='https://twitter.com/peakptsonora'
    )
    instagram = models.URLField(
        blank=True,
        null=True,
        help_text="Instagram URL",
        default='https://www.instagram.com/peakperformancecare/'
    )
    google = models.URLField(
        blank=True,
        null=True,
        help_text='Google Business URL',
        default='https://goo.gl/maps/8fe9Rymb4YeqT61DA'
    )
    youtube = models.URLField(
        blank=True,
        null=True,
        help_text="YouTube Channel URL",
        verbose_name='YouTube',
    )
    contact_panels = [
        MultiFieldPanel([
            FieldPanel('name'),
        ], heading='Business Name'),
        MultiFieldPanel([
            FieldPanel('street_address'),
            FieldPanel('mailing_address'),
            FieldPanel('city'),
            FieldPanel('state'),
            FieldPanel('zip'),
        ], heading='Address'),
        MultiFieldPanel([
            FieldPanel('phone'),
            FieldPanel('fax'),
            FieldPanel('email')
        ], heading='Phone, Fax, Email')
    ]
    hours_panels = [
        MultiFieldPanel([
            FieldPanel('sun_open'),
            FieldPanel('sun_close')
        ], heading='Sunday'),
        MultiFieldPanel([
            FieldPanel('mon_open'),
            FieldPanel('mon_close')
        ], heading='Monday'),
        MultiFieldPanel([
            FieldPanel('tue_open'),
            FieldPanel('tue_close')
        ], heading='Tuesday'),
        MultiFieldPanel([
            FieldPanel('wed_open'),
            FieldPanel('wed_close')
        ], heading='Wednesday'),
        MultiFieldPanel([
            FieldPanel('thu_open'),
            FieldPanel('thu_close')
        ], heading='Thursday'),
        MultiFieldPanel([
            FieldPanel('fri_open'),
            FieldPanel('fri_close')
        ], heading='Friday'),
        MultiFieldPanel([
            FieldPanel('sat_open'),
            FieldPanel('sat_close')
        ], heading='Saturday'),
    ]
    logo_panels = [
        ImageChooserPanel('logo_light'),
        ImageChooserPanel('logo_dark'),
        ImageChooserPanel('logo_footer'),
        ImageChooserPanel('logo_footer_alt'),
        ImageChooserPanel('logo_icon'),
        ImageChooserPanel('logo_icon_footer')
    ]
    social_panels = [
        FieldPanel('facebook'),
        FieldPanel('twitter'),
        FieldPanel('instagram'),
        FieldPanel('google'),
        FieldPanel('youtube'),
    ]
    edit_handler = TabbedInterface([
        ObjectList(contact_panels, heading='Contact Information'),
        ObjectList(hours_panels, heading='Business Hours'),
        ObjectList(logo_panels, heading='Logo'),
        ObjectList(social_panels, heading='Social Media Accounts')
    ])

    def __str__(self):
        return 'Business Settings'


@register_snippet
class Testimonial(models.Model):
    featured_quote = models.CharField(
        blank=True,
        null=True,
        max_length=500,
        help_text='Optional bold text to feature'
    )
    quote = models.TextField(
        blank=False,
        null=False,
    )
    attribution = models.CharField(
        blank=False,
        null=False,
        max_length=50
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='+',
        help_text='Optional image to add next to name'
    )

    panels = [
        FieldPanel('featured_quote', classname='full'),
        FieldPanel('quote'),
        FieldPanel('attribution'),
        ImageChooserPanel('image')
    ]

    def __str__(self):
        return self.featured_quote


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True
