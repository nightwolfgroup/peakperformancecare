from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import StreamFieldPanel, TabbedInterface, ObjectList, PageChooserPanel, FieldPanel, \
    InlinePanel, MultiFieldPanel
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page, Orderable
from wagtailmetadata.models import MetadataPageMixin


# Regulatory Home Page ------------------------------------------------------------------------------------------------>
class Regulatory(MetadataPageMixin, Page):
    template = 'regulatory/regulatory.html'
    max_count = 1
    parent_page_types = ['core.HomePage']
    subpage_types = ['regulatory.RegulatoryPolicy']

    class Meta:
        verbose_name = 'Regulatory Home Page'


class RelatedArticle(Orderable):
    page = ParentalKey('regulatory.RegulatoryPolicy', related_name='related_articles')
    related_article = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    panels = [
        PageChooserPanel('related_article')
    ]


# Regulatory Policy --------------------------------------------------------------------------------------------------->
class RegulatoryPolicy(MetadataPageMixin, Page):
    template = 'regulatory/policy.html'
    parent_page_types = ['regulatory.Regulatory']
    subpage_types = []

    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    policy = RichTextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('policy'),
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
        verbose_name = 'Regulatory Policy Page'
