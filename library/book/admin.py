from django.contrib import admin
from book.models import Book

# Register your models here.


class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'count', 'id']
    list_filter = ['name', 'author']
    search_fields = ['id', 'name', 'author__name', 'author__surname']
    fieldsets = (
        ('Constant Data', {
            'fields': ('name', 'author', 'publication_year', 'description')
        }),
        ('Additional information', {
            'classes': ['collapse'],
            'fields': ('count', 'issue_date')
        })
    )


admin.site.register(Book, BookAdmin)
