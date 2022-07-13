from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', )
    search_fields = ('username', 'email', 'role', 'bio', )
    list_filter = ('role', )
