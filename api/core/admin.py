from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.forms import MyUserChangeForm, MyUserCreationForm
from core.models import MyUser, Cities


class MyUserAdmin(UserAdmin):
    model = MyUser
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    list_display = [
        'username',
        'first_name',
        'birthday',
        'email',
        'phone',
        'city',
        'is_admin'
    ]
    list_editable = ('is_admin',)
    fieldsets = (
        (None, {
            "fields": ("username", "password")
        }),
        ('Personal info', {
            "fields": (
                ("first_name", "last_name"),
                "other_name",
                ("email", "phone"),
                "city",
                "birthday",
                "additional_info",
                "is_admin"
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
