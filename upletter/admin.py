from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin as AdminFlatPage
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _
from lands.forms import ContactForm

# Define a new FlatPageAdmin





@admin.register(FlatPage)
class FlatPageAdmin(AdminFlatPage):
    fieldsets = (
        (None, {'fields': ('url', 'title',  'content', 'sites')}),
            (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
            'enable_comments',
            'registration_required',
            'template_name',
            ),
        }),
    )

    def _changeform_view(self, *args, **kwargs):
        context = super().__changeform_view(*args, **kwargs)
        context['contact_form'] = ContactForm()
        return context

    
