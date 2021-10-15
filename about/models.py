from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel, TabbedInterface, ObjectList
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail_color_panel.edit_handlers import NativeColorPanel
from wagtail_color_panel.fields import ColorField
from wagtailmenus.models import MenuPageMixin
from wagtailmenus.panels import menupage_panel
from wagtailmetadata.models import MetadataPageMixin

from blocks.blocks import BiographyBlock, TeamBlock, PeopleWeHelpBlock, CTACircles
from blocks.choices import OPACITY_CHOICES


# About Page ---------------------------------------------------------------------------------------------------------->
class AboutPage(MetadataPageMixin, MenuPageMixin, Page):
    template = 'about/about.html'
    max_count = 1
    parent_page_types = ['core.HomePage']
    subpage_types = ['about.TeamMemberPage', 'core.LinkPage']
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
    subtitle = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )
    content = StreamField([
        ('biography', BiographyBlock()),
        ('team', TeamBlock()),
        ('people', PeopleWeHelpBlock()),
        ('cta', CTACircles())
    ])
    title_panels = Page.content_panels + [
        FieldPanel('subtitle'),
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
        verbose_name = 'About Page'


# Biography Page ------------------------------------------------------------------------------------------------------>
class TeamMemberPage(MetadataPageMixin, Page):
    template = 'about/team-member.html'
    parent_page_types = ['about.AboutPage']
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
    subtitle = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )
    team_member_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.PROTECT,
        related_name='+',
        null=True,
        blank=True,
        verbose_name='Team Member Image'
    )
    name = models.CharField(
        blank=False,
        null=True,
        max_length=40,
        help_text='Name and/or post-nominal letters if applicable. This text displays below the image.',
        verbose_name='Team Member Name'
    )
    position = models.CharField(
        blank=False,
        null=True,
        max_length=100,
        help_text='Job Title/Position in the company.',
        verbose_name='Team Member Job Title/Position'
    )
    biography = RichTextField(
        blank=False,
        null=True,
        help_text='Paragraph(s) displayed to the right of the image and title.',
        verbose_name='Team Member Biography'
    )
    title_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        MultiFieldPanel([
            ImageChooserPanel('title_image'),
            NativeColorPanel('overlay_color'),
            FieldPanel('overlay_opacity')
        ], heading='Title Image')
    ]
    content_panels = [
        ImageChooserPanel('team_member_image'),
        FieldPanel('name'),
        FieldPanel('position'),
        FieldPanel('biography')
    ]
    edit_handler = TabbedInterface([
        ObjectList(title_panels, heading='Title & Header'),
        ObjectList(content_panels, heading='Team Member Information'),
        ObjectList(MetadataPageMixin.promote_panels, heading='SEO/Menu'),
        ObjectList(Page.settings_panels, heading='Page Settings', classname='settings')
    ])

    class Meta:
        verbose_name = 'Team Member Page'
