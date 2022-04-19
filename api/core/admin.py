from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.forms import MyUserChangeForm, MyUserCreationForm
from core.models import MyUser, Cities


class MyUserAdmin(UserAdmin):
    model = MyUser
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    list_display = [
        'email',
        'first_name',
        'birthday',
        'phone',
        'city',
        'is_admin'
    ]
    list_display_links = ('email',)
    list_editable = ('is_admin',)
    ordering = ('date_joined',)
    fieldsets = (
        (None, {
            "fields": ('email', 'password')
        }),
        ('Personal info', {
            "fields": (
                ("first_name", "last_name", "is_admin"),
                "other_name",
                ("phone", "city"),
                "birthday",
                "additional_info"
            )
        }),
        ('Permissions', {
            'classes': ('collapse',),
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions"
            )
        }),
        ('Important dates', {
            'classes': ('collapse',),
            "fields": ("last_login", "date_joined")
        }),
    )


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Cities)
