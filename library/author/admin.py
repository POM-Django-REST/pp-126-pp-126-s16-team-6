from django.contrib import admin
from author.models import Author

# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    fields = [('name', 'surname'), 'patronymic']
    list_display = ['surname', 'name', 'patronymic', 'id']
    search_fields = ['name', 'surname', 'patronymic', 'id']
    list_filter = ['surname', 'patronymic']

admin.site.register(Author, AuthorAdmin)
