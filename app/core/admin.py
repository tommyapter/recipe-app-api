from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from core import models


# import the default Django user admin and we just need to change some of the class variables to support our custom user admin.
# because there's still a few changes that we need to make to our Django admin class to support our custom user model the Edit Page won't work in its current state. So we're going to make some changes to make sure that it does work.
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # None because this is the title for the section. Each one of these brackets is a section
        (_('Personal Info'), {'fields': ('name',)}),  # make sure you add this comma ('name',) because otherwise it thinks this is just a string and it won't work.
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, UserAdmin)
