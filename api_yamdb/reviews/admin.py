from django.contrib import admin

from .models import Review, Comment


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'text', 'title',)
    search_fields = ("text", "author__username",)
    list_filter = ('score', 'pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'pub_date', 'author', 'text',)
    search_fields = ("text", "author__username",)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
