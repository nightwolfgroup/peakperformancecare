from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from django.forms import CheckboxSelectMultiple
from django.shortcuts import render
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList, FieldPanel, StreamFieldPanel
from wagtail.contrib.routable_page.models import route, RoutablePageMixin
from wagtail.core.blocks import RichTextBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtailmetadata.models import MetadataPageMixin
from blocks.blocks import PodcastPlayerBlock, PodcastEpisodeBlock, BlogButtonBlock, BlockquoteBlock


# Blog Home ----------------------------------------------------------------------------------------------------------->
class Blog(RoutablePageMixin, MetadataPageMixin, Page):
    template = 'blog/blog.html'
    max_count = 1
    parent_page_types = ['core.HomePage']
    subpage_types = ['blog.BlogPost']

    edit_handler = TabbedInterface([
        ObjectList(Page.content_panels, heading='Title & Header'),
        ObjectList(MetadataPageMixin.promote_panels, heading='SEO/Menu'),
        ObjectList(Page.settings_panels, heading='Page Settings', classname='settings')
    ])

    class Meta:
        verbose_name = 'Blog Home Page'

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        all_posts = BlogPost.objects.live().public().order_by('-first_published_at')
        paginator = Paginator(all_posts, 5)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context['posts'] = posts
        return context

    @route(r"^category/(?P<cat_slug>[-\w]*)/$", name='category_view')
    def category_view(self, request, cat_slug):
        context = self.get_context(request)
        try:
            category = BlogCategory.objects.get(slug=cat_slug)
        except Exception:
            category = None
        if category is None:
            pass

        context['posts'] = BlogPost.objects.live().public().filter(categories__in=[category])
        context['page_category'] = category
        return render(request, 'blog/blog.html', context)


# Blog Post ----------------------------------------------------------------------------------------------------------->
class BlogPost(MetadataPageMixin, Page):
    template = 'blog/post.html'
    parent_page_types = ['blog.Blog']
    subpage_types = []
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True, related_name='blog_post')
    tags = ClusterTaggableManager(through='blog.BlogPageTag', blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='blog_post'
    )
    image = models.ForeignKey(
        'wagtailimages.image',
        on_delete=models.PROTECT,
        verbose_name='Cover Image'
    )
    content = StreamField([
        ('content_block', RichTextBlock(label='Content Block')),
        ('podcast', PodcastPlayerBlock()),
        ('podcast_episode', PodcastEpisodeBlock()),
        ('button', BlogButtonBlock()),
        ('blockquote', BlockquoteBlock())
    ])
    content_panels = [
        ImageChooserPanel('image'),
        FieldPanel('author'),
        FieldPanel('categories', widget=CheckboxSelectMultiple),
        FieldPanel('tags'),
        StreamFieldPanel('content'),
    ]
    edit_handler = TabbedInterface([
        ObjectList(Page.content_panels + content_panels, heading='Post Content'),
        ObjectList(MetadataPageMixin.promote_panels, heading='SEO/Menu'),
        ObjectList(Page.settings_panels, heading='Page Settings', classname='settings')
    ])

    def save(self, *args, **kwargs):
        key = make_template_fragment_key('latest_posts', [self.id])
        cache.delete(key)
        key2 = make_template_fragment_key('post_preview', [self.id])
        cache.delete(key2)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Blog Post'


# Blog Categories & Tags ---------------------------------------------------------------------------------------------->
@register_snippet
class BlogCategory(models.Model):
    """Blog category for a snippet."""
    name = models.CharField(max_length=255)
    slug = AutoSlugField(
        verbose_name="Slug URL",
        populate_from='name',
        max_length=255,
        help_text='A slug URL to identify posts by this category',
        unique=True
    )
    panels = [
        FieldPanel("name")
    ]

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPost', related_name='post_tags')
