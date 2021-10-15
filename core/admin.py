from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from core.models import Testimonial


class TestimonialAdmin(ModelAdmin):
    model = Testimonial
    menu_label = 'Testimonials'
    menu_icon = 'fa-quote-right'
    menu_order = 103
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('featured_quote', 'attribution')


modeladmin_register(TestimonialAdmin)
