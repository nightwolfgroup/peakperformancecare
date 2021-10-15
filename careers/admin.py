from careers.models import Application
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register


class ApplicationAdmin(ModelAdmin):
    model = Application
    menu_label = 'Job Applicants'
    menu_icon = 'fa-medkit'
    menu_order = 110
    add_to_settings_menu = False
    exclude_from_explorer = False
    export_filename = 'job_applicants'
    list_export = (
        'first_name',
        'last_name',
        'position',
        'phone',
        'email',
        'applicant_city',
        'eligible',
        'transportation',
        'cannot_work',
        'education',
        'start_date',
        'ref_name',
        'ref_phone',
        'ref_relation',
        'ref_years'
    )
    list_display = (
        '__str__',
        'position',
        'phone',
        'email',
        'applicant_city',
        'education',
        'resume',
        'cover_letter'
    )
    list_filter = ('position', 'eligible', 'transportation', 'cannot_work', 'education')
    search_fields = ('first_name', 'last_name', 'email')


modeladmin_register(ApplicationAdmin)
