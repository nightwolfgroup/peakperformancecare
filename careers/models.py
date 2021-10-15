from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList, FieldRowPanel, FieldPanel, MultiFieldPanel, \
    StreamFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail_color_panel.edit_handlers import NativeColorPanel
from wagtail_color_panel.fields import ColorField
from wagtailmetadata.models import MetadataPageMixin

from blocks.choices import OPACITY_CHOICES
from careers.choices import JOB_POST_STATUS_CHOICES, JOB_TYPE_CHOICES, SALARY_UNIT_CHOICES


# Careers Home -------------------------------------------------------------------------------------------------------->
class Careers(MetadataPageMixin, Page):
    template = 'careers/careers.html'
    max_count = 1
    parent_page_types = ['core.HomePage']
    subpage_types = ['careers.CareerPost']
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
    title_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('title_image'),
            NativeColorPanel('overlay_color'),
            FieldPanel('overlay_opacity')
        ], heading='Title Image')
    ]
    edit_handler = TabbedInterface([
        ObjectList(title_panels, heading='Title & Header'),
        ObjectList(MetadataPageMixin.promote_panels, heading='SEO/Menu'),
        ObjectList(Page.settings_panels, heading='Page Settings', classname='settings')
    ])

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['accepting_applications'] = CareerPost.objects.filter(status='Accepting Applications').live().public()
        context['interviewing'] = CareerPost.objects.filter(status='Interviewing Applicants').live().public()
        context['position_filled'] = CareerPost.objects.filter(status='Position Filled').live().public()
        return context

    class Meta:
        verbose_name = 'Careers Home Page'


# File format validator for resume and cover letter upload ------------------------------------------------------------>
def validate_file_format(value):
    if value.file.content_type != \
            'application/pdf' or \
            'application/msword' \
            or 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        raise ValidationError(u'File is not a valid file type.')


# Applicant model ----------------------------------------------------------------------------------------------------->
class Application(models.Model):
    position = models.CharField(
        max_length=100,
        blank=False,
        help_text='Position applied for'
    )
    first_name = models.CharField(
        max_length=50,
        blank=False,
        help_text='Applicant first name'
    )
    last_name = models.CharField(
        max_length=50,
        blank=False,
        help_text='Applicant last name'
    )
    phone = models.CharField(
        max_length=12,
        blank=False,
        help_text='Applicant phone number'
    )
    email = models.EmailField(
        blank=False,
        help_text='Applicant email address'
    )
    applicant_address = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Address'
    )
    applicant_city = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='City'
    )
    applicant_state = models.CharField(
        max_length=2,
        blank=False,
        verbose_name='State'
    )
    applicant_zip = models.IntegerField(
        blank=False,
        verbose_name='Zip code'
    )
    eligible = models.CharField(
        max_length=3,
        blank=False,
        verbose_name='Eligibility to work in U.S.?',
        help_text='Are you able to provide proof you are eligible to work in the U.S.?'
    )
    transportation = models.CharField(
        max_length=3,
        blank=False,
        verbose_name='Reliable transportation?',
        help_text='Do you have reliable transportation to get you to and from work?'
    )
    cannot_work = models.CharField(
        max_length=3,
        blank=False,
        verbose_name='Time applicant cannot work?',
        help_text='Is there any time that you cannot work?'
    )
    ref_name = models.CharField(
        max_length=100,
        blank=False,
        verbose_name='Reference Name',
    )
    ref_phone = models.CharField(
        max_length=12,
        blank=False,
        verbose_name='Reference Phone Number'
    )
    ref_relation = models.CharField(
        max_length=200,
        blank=False,
        verbose_name='Relationship to Reference'
    )
    ref_years = models.CharField(
        max_length=50,
        blank=False,
        verbose_name='Years applicant has known reference'
    )
    education = models.CharField(
        max_length=50,
        blank=False,
        verbose_name='Highest level of education'
    )
    start_date = models.DateField(
        blank=False,
        verbose_name='Earliest start date'
    )
    resume = models.FileField(
        blank=False,
        upload_to='career_applicants/resume',
        validators=[validate_file_format],
    )
    cover_letter = models.FileField(
        blank=True,
        upload_to='career_applicants/resume',
        validators=[validate_file_format]
    )
    captcha = models.TextField(blank=False)

    def __str__(self):
        return self.first_name + ' ' + str(self.last_name)

    panels = [
        FieldRowPanel([
            FieldPanel('first_name'),
            FieldPanel('last_name')
        ], heading='Applicant Name'),
        FieldRowPanel([
            FieldPanel('phone'),
            FieldPanel('email'),
        ], heading='Contact Information'),
        FieldRowPanel([
            FieldPanel('applicant_address'),
            FieldPanel('applicant_city'),
            FieldPanel('applicant_state'),
            FieldPanel('applicant_zip')
        ], heading='Address'),
        MultiFieldPanel([
            FieldPanel('eligible'),
            FieldPanel('transportation'),
            FieldPanel('cannot_work'),
            FieldPanel('education'),
            FieldPanel('start_date')
        ], heading='Screening Questions'),
        MultiFieldPanel([
            FieldPanel('ref_name'),
            FieldPanel('ref_phone'),
            FieldPanel('ref_years'),
            FieldPanel('ref_relation')
        ], heading='Reference'),
        MultiFieldPanel([
            FieldPanel('resume'),
            FieldPanel('cover_letter')
        ], heading='Resume/Cover Letter'),
    ]

    class Meta:
        verbose_name = 'Job Applicant'
        verbose_name_plural = 'Job Applicants'


# Career Post --------------------------------------------------------------------------------------------------------->
class CareerPost(MetadataPageMixin, Page):
    template = 'careers/post.html'
    parent_page_types = ['careers.Careers']
    subpage_types = []

    updated_on = models.DateTimeField(
        auto_now=True
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )
    valid_until = models.DateTimeField(
        blank=False,
        null=True
    )
    status = models.CharField(
        choices=JOB_POST_STATUS_CHOICES,
        max_length=255
    )
    position_type = models.CharField(
        choices=JOB_TYPE_CHOICES,
        max_length=255)
    salary = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Compensation ($)')
    salary_unit = models.CharField(
        choices=SALARY_UNIT_CHOICES,
        max_length=255,
        blank=True,
        verbose_name='Compensation Unit'
    )
    content = RichTextField(blank=False, null=True)
    content_panels = [
        MultiFieldPanel([
            FieldPanel('status'),
            FieldPanel('position_type'),
            FieldPanel('valid_until')
        ], heading="Position Details"),
        MultiFieldPanel([
            FieldPanel('salary'),
            FieldPanel('salary_unit')
        ], heading="Compensation Details (Optional)"),
        FieldPanel('content'),
    ]
    form_panels = [
        StreamFieldPanel('application_form')
    ]
    edit_handler = TabbedInterface([
        ObjectList(Page.content_panels + content_panels, heading='Career/Job Post'),
        ObjectList(MetadataPageMixin.promote_panels, heading='SEO/Menu'),
        ObjectList(Page.settings_panels, heading='Page Settings', classname='settings')
    ])

    def serve(self, request, *args, **kwargs):

        from careers.forms import ApplicationForm

        if request.method == 'POST':
            form = ApplicationForm(request.POST, request.FILES or None, initial={'position': str(self.title)})
            if form.is_valid():
                # Clean
                resume = request.FILES['resume']
                cover_letter = request.FILES['cover_letter']
                data = form.cleaned_data
                Application.objects.create(**data)
                # Email
                html_email = render_to_string('email/applicant-alert.html', {'data': data})
                text_email = strip_tags(html_email)
                email = EmailMultiAlternatives(
                    f'New Application from {data["first_name"]} {data["last_name"]}',
                    text_email,
                    'Peak Performance Care Physical Therapy <info@peakperformancecare.com>',
                    ['info@peakperformancecare.com'],
                )
                email.attach(resume.name, resume.read(), resume.content_type)
                email.attach(cover_letter.name, cover_letter.read(), cover_letter.content_type)
                email.fail_silently = True
                email.send()
                # Reload
                messages.success(request, 'Your application has been received!')
                return super().serve(request)
            else:
                # If Error in Form
                messages.error(request, 'There seems to have been an error, '
                                        'please correct any missing or invalid fields.')
                context = {'self': self, 'page': self, 'form': form}
                return render(request, 'careers/post.html', context)
        else:
            form = ApplicationForm(initial={'position': str(self.title)})
            context = {'self': self, 'page': self, 'form': form}
            return render(request, 'careers/post.html', context)

    class Meta:
        verbose_name = 'Career/Job Post'

