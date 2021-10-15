from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from .choices import FE_ICONS, OPACITY_CHOICES, BUTTON_CHOICES
from wagtail_color_panel.blocks import NativeColorBlock
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList


# Internal vs. External Link Logic ------------------------------------------------------------------------------------>
class LinkValue(blocks.StructValue):
    def url(self) -> str:
        internal_page = self.get('internal_page')
        external_link = self.get('external_link')
        if internal_page:
            return internal_page.url
        elif external_link:
            return external_link
        return ""


class Link(blocks.StructBlock):
    """ Example use: {{ link.url }} """
    link_text = blocks.CharBlock(
        max_length=50,
        label='Button/Link Text'
    )
    internal_page = blocks.PageChooserBlock(
        required=False,
        help_text='Point the link to an internal page.',
        label='Internal Page Link'
    )
    external_link = blocks.URLBlock(
        required=False,
        help_text='Point the link to an external page.',
        label='External Page Link'
    )
    new_tab = blocks.BooleanBlock(
        required=False,
        help_text='Check if you would like the link to open in a new tab when clicked.',
        label='Open Link In New Tab?'
    )
    
    class Meta:
        value_class = LinkValue

    def clean(self, value):
        internal_page = value.get('internal_page')
        external_link = value.get('external_link')
        errors = {}
        if internal_page and external_link:
            errors['internal_page'] = ErrorList(['Please select either an internal page OR an external link.'])
            errors['external_link'] = ErrorList(['Please select either an internal page OR an external link.'])

        if errors:
            raise ValidationError("Validation error", params=errors)
        return super().clean(value)


class Button(blocks.StructBlock):
    """ Example use: {{ button.url }} """
    button_color = blocks.ChoiceBlock(
        choices=BUTTON_CHOICES,
        default='btn-primary',
        required=True
    )
    button_text = blocks.CharBlock(
        max_length=50,
        label='Button/Link Text'
    )
    internal_page = blocks.PageChooserBlock(
        required=False,
        help_text='Point the link to an internal page.',
        label='Internal Page Link'
    )
    external_link = blocks.URLBlock(
        required=False,
        help_text='Point the link to an external page.',
        label='External Page Link'
    )
    new_tab = blocks.BooleanBlock(
        required=False,
        help_text='Check if you would like the link to open in a new tab when clicked.',
        label='Open Link In New Tab?'
    )

    class Meta:
        value_class = LinkValue

    def clean(self, value):
        internal_page = value.get('internal_page')
        external_link = value.get('external_link')
        errors = {}
        if internal_page and external_link:
            errors['internal_page'] = ErrorList(['Please select either an internal page OR an external link.'])
            errors['external_link'] = ErrorList(['Please select either an internal page OR an external link.'])

        if errors:
            raise ValidationError("Validation error", params=errors)
        return super().clean(value)


# Title Blocks -------------------------------------------------------------------------------------------------------->
class MainTitleBlock(blocks.StructBlock):
    image = ImageChooserBlock(
        required=True,
        help_text='Image to display as the background of this title block.'
    )
    image_overlay_color = NativeColorBlock(
        required=True,
        default='#100f0a'
    )
    overlay_opacity = blocks.ChoiceBlock(
        choices=OPACITY_CHOICES,
        help_text='The larger the number, the more intense the image overlay will become.',
        default='.7',
        label='Image Overlay Opacity (%)'
    )
    company_name = blocks.CharBlock(
        required=False,
        max_length=50,
        help_text='Optional text to display above the page title, not required to be the company name.',
        default='PEAK PERFORMANCE CARE'
    )
    title = blocks.CharBlock(
        required=True,
        max_length=200,
        help_text='Main title text',
        default='We Help Active Adults Who Want To Get Back To The Activities They Love Without Medication & Surgery'
    )
    subtitle = blocks.CharBlock(
        required=False,
        max_length=100,
        help_text='Optional text to display below the title',
        default="Get The Healthy Lifestyle You've Always Wanted!"
    )

    class Meta:
        template = 'blocks/title/title.html'
        label = 'Home Page Title'
        icon = 'fa-star'
        group = 'Titles'


class PageTitleBlock(blocks.StructBlock):
    image = ImageChooserBlock(
        required=False,
        help_text='Optional image to display as the background title'
    )
    image_overlay_color = NativeColorBlock(
        required=True,
        default='#100f0a'
    )
    overlay_opacity = blocks.ChoiceBlock(
        choices=OPACITY_CHOICES,
        help_text='The larger the number, the more intense the image overlay will become.',
        default='.7',
        label='Image Overlay Opacity (%)'
    )
    title = blocks.CharBlock(
        required=True,
        max_length=255,
        help_text='Main title of the page'
    )
    subtitle = blocks.CharBlock(
        required=False,
        max_length=255,
        help_text='Optional text to display below the title'
    )

    class Meta:
        template = 'blocks/title/page-title.html'
        label = 'Page Title'
        icon = 'fa-star'
        group = 'Titles'
        help_text = 'Simple page title with a banner image and overlay text.'


class ServiceTitle(blocks.StructBlock):
    image = ImageChooserBlock(
        required=False,
        help_text='Optional image to display as the background title'
    )
    title = blocks.CharBlock(
        required=False,
        max_length=50,
        help_text='Main title of the page'
    )
    subtitle = blocks.RichTextBlock(
        required=False,
        help_text='Optional text to display below the title'
    )
    button_text = blocks.CharBlock(
        required=False,
        max_length=50,
        help_text='Text to display inside of a button below the subtitle',
        default='Yes! I Want the FREE Guide!'
    )
    button_link = blocks.PageChooserBlock(
        required=True,
        help_text='Page the button will link to when clicked'
    )
    guide_image = ImageChooserBlock(
        required=True,
        help_text='Guide image will display in an iPhone frame'
    )
    discovery_title = blocks.CharBlock(
        required=True,
        help_text='Text displayed to the left of the guide image.',
        default="In This Guide You'll Discover..."
    )
    discoveries = blocks.ListBlock(
        blocks.StructBlock([
            ('heading', blocks.CharBlock(
                required=True,
                max_length=255,
                help_text='Bold text at top of discovery block'
            )),
            ('subtext', blocks.CharBlock(
                required=False,
                max_length=255,
                help_text='Optional text to display below the heading'
            )),
        ], icon='fa-search'), label="In this guide you'll discover..."
    )

    class Meta:
        template = 'blocks/title/service-title.html'
        label = 'Service Page Title'
        icon = 'fa-medkit'
        group = 'Titles'
        help_text = 'Specialty title with phone frame.'


class ContactPageTitle(blocks.StructBlock):
    background_image = ImageChooserBlock(
        required=False
    )
    overlay_opacity = blocks.IntegerBlock(
        max_value=9,
        min_value=0,
        default=8
    )
    overlay_color = NativeColorBlock(
        required=True,
        default='#000000'
    )
    heading = blocks.CharBlock(
        required=True,
        max_length=255
    )
    subheading = blocks.CharBlock(
        required=False,
        max_length=255
    )
    infusionsoft_form = blocks.RawHTMLBlock(
        required=True,
        help_text='Insert the entire JavaScript snippet from Infusionsoft here.'
    )

    class Meta:
        template = 'blocks/title/contact-title.html'
        label = 'Contact Page Title'
        icon = 'fa-comments'
        group = 'Titles'
        help_text = 'Contact page title with Infusionsoft form integration.'


# Content Blocks ------------------------------------------------------------------------------------------------------>
class BiographyBlock(blocks.StructBlock):
    image = ImageChooserBlock(
        required=False,
        label='Staff Image'
    )
    name = blocks.CharBlock(
        required=False,
        max_length=40,
        help_text='Name and/or post-nominal letters if applicable. This text displays below the image.'
    )
    position = blocks.CharBlock(
        required=False,
        max_length=255,
        help_text="Text displayed below the person's name."
    )
    title = blocks.CharBlock(
        required=False,
        max_length=255,
        help_text='Optional text displayed above the biography paragraph(s).'
    )
    bio = blocks.RichTextBlock(
        required=False,
        help_text='Paragraph(s) displayed to the right of the image and title.'
    )

    class Meta:
        template = 'blocks/content/biography.html'
        help_text = 'A Biography block with a large image to the left of paragraph(s).'
        label = 'Biography with Image'
        icon = 'fa-user-circle-o'


class TelehealthBlock(blocks.StructBlock):
    image = ImageChooserBlock(
        required=True,
        help_text='Image displayed to the left of the button and title'
    )
    heading = blocks.CharBlock(
        required=False,
        max_length=50,
        help_text='Optional heading to display above the button',
        default='Telehealth Services'
    )
    button = Button(
        required=True
    )

    class Meta:
        template = 'blocks/content/telehealth.html'
        help_text = 'Large telehealth cover image with a button to link to your telehealth waiting room.'
        label = 'Telehealth Button'
        icon = 'fa-video-camera'


class TeamBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        max_length=100,
        default='Our Team'
    )

    def get_context(self, request, *args, **kwargs):
        from about.models import TeamMemberPage
        context = super().get_context(request, *args, **kwargs)
        team_members = TeamMemberPage.objects.live().public()
        context['team_members'] = team_members
        return context

    class Meta:
        template = 'blocks/content/team.html'
        help_text = 'Team members block with images in cards which link to their respective bio pages. ' \
                    'Automatically generated from team member pages.'
        label = 'Our Team'
        icon = 'fa-users'


class PeopleWeHelpBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        max_length=80,
        help_text='Section title',
        default='People We Help'
    )
    bullet_icon = blocks.ChoiceBlock(
        choices=FE_ICONS,
        required=True,
        help_text='Icon displayed as the bullet for each item',
        default='fe-check-circle'
    )
    people = blocks.ListBlock(
        blocks.StructBlock([
            ('heading', blocks.CharBlock(
                required=True,
                max_length=50
            )),
            ('text', blocks.RichTextBlock(
                required=True
            ))
        ], icon='fa-user'), label='People We Help'
    )

    class Meta:
        template = 'blocks/content/bulleted-list.html'
        help_text = 'People We Help Block'
        label = 'People We Help'
        icon = 'fa-info-circle'


class VideoSplitBlock(blocks.StructBlock):
    image = ImageChooserBlock(
        required=True,
        help_text='Image displayed as the video icon'
    )
    action_text = blocks.CharBlock(
        required=False,
        help_text='Optional text to display below the play button of the video',
        default='Click me to watch video!'
    )
    video_link = blocks.URLBlock(
        required=True,
        help_text='Link to video from a service such as YouTube or Vimeo'
    )
    heading = blocks.CharBlock(
        required=True,
        help_text='Title text to display to the right of the video thumbnail'
    )
    list_items = blocks.ListBlock(
        blocks.StructBlock([
            ('icon', blocks.ChoiceBlock(
                choices=FE_ICONS,
                help_text='Icon to display as the bullet for the list item.'
            )),
            ('heading', blocks.CharBlock(
                required=True,
                help_text='List item heading displayed below the section title'
            )),
            ('subtext', blocks.TextBlock(
                required=False,
                help_text='Optional text displayed below the list item heading'
            ))
        ])
    )

    class Meta:
        template = 'blocks/content/video-split.html'
        label = 'Video Thumbnail w/ List'
        help_text = 'A video thumbnail with text displayed to the right of the video.'
        icon = 'fa-play'


class PersonalMessageBlock(blocks.StructBlock):
    heading = blocks.RichTextBlock(
        required=True,
        help_text='Heading text placed before the personal message'
    )
    image = ImageChooserBlock(
        required=True,
        help_text='Staff image displayed to the left of the personal message'
    )
    message = blocks.RichTextBlock(
        required=True
    )
    button = blocks.BooleanBlock(
        required=False,
        default=True,
        help_text='Check this box if you would like a button to display at the bottom of the personal message.'
    )
    button_text = blocks.CharBlock(
        required=False,
        default='Yes! I Want the FREE Guide!'
    )

    class Meta:
        template = 'blocks/content/personal-message.html'
        label = 'Personal Message'
        icon = 'fa-comment'


class IconCardsBlock(blocks.StructBlock):
    cards = blocks.ListBlock(
        blocks.StructBlock([
            ('icon', blocks.ChoiceBlock(
                choices=FE_ICONS,
                required=False,
                help_text='Icon to display at the top of the card'
            )),
            ('icon_color', NativeColorBlock(
                default='#180070'
            )),
            ('title', blocks.CharBlock(
                required=True,
                max_length=30
            )),
            ('subtitle', blocks.CharBlock(
                required=False,
                max_length=255,
                help_text='Optional text to display beneath the title of the card'
            )),
            ('button', Button(
                required=True
            ))
        ], icon='fa-plus-square-o'), label='Card'
    )

    class Meta:
        template = 'blocks/content/cards.html'
        label = 'Icon Cards'
        icon = 'fa-info-circle'


class PodcastPlayerBlock(blocks.StructBlock):
    class Meta:
        template = 'blocks/content/podcast-player.html'
        label = 'Podcast Widget'
        icon = 'fa-podcast'
        help_text = 'Your podcast episodes will automatically pull into the player from Buzzsprout'


class PodcastEpisodeBlock(blocks.StructBlock):
    embed_code = blocks.RawHTMLBlock(
        required=True,
        help_text='Place the entire embed code from Buzzsprout here'
    )

    class Meta:
        template = 'blocks/content/podcast-single.html'
        label = 'Podcast Widget (Single Episode)'
        icon = 'fa-podcast'


class BlogButtonBlock(blocks.StructBlock):
    button = Button(
        required=True
    )

    class Meta:
        template = 'blocks/content/blog-button.html'
        label = 'Button'
        icon = 'fa-external-link'
        help_text = 'A button that will display between blog post content blocks'


class ModalFormBlock(blocks.StructBlock):
    modal_title = blocks.CharBlock(
        required=False,
        help_text='Title of pop up window that contains the form'
    )
    infusionsoft_link = blocks.URLBlock(
        required=True,
        help_text='Input the link to the Infusionsoft form here'
    )

    class Meta:
        template = 'blocks/forms/modal-form.html'
        label = 'Infusionsoft Form'
        icon = 'fa-check-square-o'
        help_text = 'A modal pop-up window containing a form linked to Infusionsoft'


class VideoShowcaseBlock(blocks.StructBlock):
    video_groups = blocks.ListBlock(
        blocks.StructBlock([
            ('group_title', blocks.CharBlock(
                required=True,
                max_length=25,
                label='Category Title'
            )),
            ('group_videos', blocks.ListBlock(
                blocks.StructBlock([
                    ('thumbnail', ImageChooserBlock(
                        required=True,
                        label='Video Thumbnail'
                    )),
                    ('heading', blocks.CharBlock(
                        required=True,
                        max_length=50,
                        label='Video Title'
                    )),
                    ('form_title', blocks.CharBlock(
                        required=True,
                        max_length=255
                    )),
                    ('form', blocks.RawHTMLBlock(
                        required=True,
                        help_text='Place the entire Infusionsoft embed code snippet here.',
                        label='Infusionsoft Form'
                    ))
                ], icon='fa-youtube-play'),
                help_text='Videos that belong to this category.',
                label='Videos'
            ))
        ], icon='fa-object-group'),
        label='Video Categories',
        help_text='Each video group will add a button at the top of the gallery to filter by the videos in the group'
    )

    class Meta:
        template = 'blocks/content/video-showcase.html'
        label = 'Video Showcase'
        icon = 'fa-youtube'
        help_text = 'A block of videos in a grid layout'


class BlockquoteBlock(blocks.StructBlock):
    block_title = blocks.CharBlock(
        required=False,
        max_length=200,
        help_text='Optional title to display above the blockquote'
    )
    quote = blocks.RichTextBlock(
        required=True
    )
    attribution = blocks.CharBlock(
        max_length=500,
        required=True
    )

    class Meta:
        template = 'blocks/content/blockquote.html'
        label = 'Blockquote'
        icon = 'openquote'
        help_text = 'A blockquote within a rounded color background with quotation mark icon'


class FreeReportBlock(blocks.StructBlock):
    subtitle = blocks.RichTextBlock(required=True)
    guide_image = ImageChooserBlock(
        required=True,
        help_text='Guide image will display in an iPhone frame'
    )
    discovery_title = blocks.CharBlock(
        required=True,
        help_text='Text displayed to the left of the guide image.',
        default="In This Guide You'll Discover..."
    )
    button_text = blocks.CharBlock(
        required=False,
        max_length=50,
        help_text='Text to display inside of a button below the subtitle',
        default='Yes! I Want the FREE Guide!'
    )
    discoveries = blocks.ListBlock(
        blocks.StructBlock([
            ('heading', blocks.CharBlock(
                required=True,
                max_length=255,
                help_text='Bold text at top of discovery block'
            )),
            ('subtext', blocks.CharBlock(
                required=False,
                max_length=255,
                help_text='Optional text to display below the heading'
            )),
        ], icon='fa-search'), label="In this guide you'll discover..."
    )

    class Meta:
        template = 'blocks/content/free-report.html'
        label = 'Free Report'
        icon = 'fa-book'


# Call To Action Blocks ----------------------------------------------------------------------------------------------->
class CTACards(blocks.StructBlock):
    heading = blocks.CharBlock(
        max_length=100,
        required=False,
        help_text='Text displayed above all CTA cards.',
        default='Want Help Deciding If Physical Therapy Is Right For You?'
    )
    background_color = NativeColorBlock(
        required=True,
        default='#180070'
    )
    cards = blocks.ListBlock(
        blocks.StructBlock([
            ('icon', blocks.ChoiceBlock(
                required=False,
                choices=FE_ICONS,
                help_text='Optional icon to display at the top of the card.'
            )),
            ('heading', blocks.CharBlock(
                required=True,
                max_length=100,
                help_text='Bold text to display at the top of the CTA card.'
            )),
            ('content', blocks.RichTextBlock(
                required=True,
                help_text='Text to display below the title within the CTA card.'
            )),
            ('button', Button(
                required=True,
            ))
        ], icon='fa-window-restore'), label='Call to Action Cards'
    )

    class Meta:
        template = 'blocks/cta/cards.html'
        label = 'CTA Cards'
        icon = 'fa-bullhorn'
        help_text = 'Scrolling carousel with cards containing an icon, title, text, and a CTA button.'


class CTACircles(blocks.StructBlock):
    heading = blocks.CharBlock(
        required=True,
        max_length=100,
        help_text='Heading text to display to the right of the CTA links.',
        default='Want To Get Relief Faster?'
    )
    subtext = blocks.CharBlock(
        required=False,
        max_length=500,
        help_text='Optional text to display below the heading.',
        default='Choose an option that works best for you.'
    )
    links = blocks.ListBlock(
        blocks.StructBlock([
            ('icon', ImageChooserBlock(
                required=True,
                help_text='Icon to display inside of a circle to act as a link.'
            )),
            ('link', Link(
                required=True
            ))
        ], icon='fa-link'), label='CTA Link'
    )
    background_image = ImageChooserBlock(required=False)

    class Meta:
        template = 'blocks/cta/circles.html'
        label = 'CTA Circles'
        icon = 'fa-bullhorn'
        help_text = 'A call to action with icons set inside circles displayed to the left of a heading.'


class CTAGuides(blocks.StructBlock):
    title = blocks.CharBlock(
        required=True,
        max_length=150,
        help_text='Title text displayed above the guide images',
        default='Need Some Tips To Get Relief Right Now?'
    )
    subtitle = blocks.RichTextBlock(
        required=False,
        help_text='Optional text to display below the title.'
    )
    guides = blocks.ListBlock(
        blocks.StructBlock([
            ('image', ImageChooserBlock(
                required=True
            )),
            ('text', blocks.CharBlock(
                max_length=50,
                required=False,
                help_text='Regular weight text displayed above the button.'
            )),
            ('button', Button(
                required=True,
                help_text='Page the guide button will link to when clicked.'
            )),
        ], icon='fa-book'), label='Guide Image with Link'
    )

    class Meta:
        template = 'blocks/cta/guides.html'
        label = 'Guides CTA'
        icon = 'fa-book'
        help_text = 'A free guides CTA, contains an image of the guide and ' \
                    'the guide title, which links to a page to obtain the guide.'


# Testimonial Blocks -------------------------------------------------------------------------------------------------->
class TestimonialCards(blocks.StructBlock):
    title = blocks.CharBlock(max_length=30, required=True, default='Testimonials')

    def get_context(self, request, *args, **kwargs):
        from core.models import Testimonial
        context = super().get_context(request, *args, **kwargs)
        testimonials = Testimonial.objects.all()
        context['testimonials'] = testimonials
        return context

    class Meta:
        template = 'blocks/testimonials/testimonials.html'
        label = 'Testimonial Cards'
        icon = 'fa-quote-right'
        help_text = 'Testimonials are pulled in from the Testimonials menu automatically'


# Legal Page Blocks --------------------------------------------------------------------------------------------------->
class LegalBlock(blocks.StructBlock):
    page_content = blocks.RichTextBlock(
        required=False
    )
    related_articles = blocks.ListBlock(
        blocks.StructBlock([
            ('related_article_name', blocks.CharBlock(
                required=False,
                max_length=100
            )),
            ('related_article_link', blocks.PageChooserBlock(
                required=False
            ))
        ], icon='fa-window-restore'), label='Related Articles'
    )

    class Meta:
        template = 'blocks/content/legal-block.html'
        label = 'Legal Block (Full Page)'
        icon = 'fa-gavel'
