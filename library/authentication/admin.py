from django.contrib import admin
from authentication.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'middle_name', 'last_name', 'role', 'id']
    search_fields = ['id', 'email', 'role', 'first_name', 'last_name']
    list_filter = ['email', 'role']
    fieldsets = (
        (None, {
            'fields': ('email', 'first_name', 'last_name', 'middle_name',
                       'role', 'last_login')
        }),
        ('Advance options', {
            'classes': ['collapse'],
            'fields': ('is_active', 'is_staff', 'is_superuser')
        })
    )


admin.site.register(CustomUser, CustomUserAdmin)
