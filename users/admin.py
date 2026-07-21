from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for Django's default User model.
    """

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "date_joined",
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "groups",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    readonly_fields = (
        "date_joined",
        "last_login",
    )

    fieldsets = (
        (None, {
            "fields": (
                "username",
                "password",
            ),
        }),
        ("Personal Info", {
            "fields": (
                "first_name",
                "last_name",
                "email",
            ),
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        }),
        ("Important dates", {
            "fields": (
                "last_login",
                "date_joined",
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": (
                "wide",
            ),
            "fields": (
                "username",
                "email",
                "password1",
                "password2",
            ),
        }),
    )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
