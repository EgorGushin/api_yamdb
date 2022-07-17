from django.contrib import admin

from .mixins import DisplayEmptyFielsdMixin
from .models import (Category, Comment,
                     Genre, Review,
                     Title, User)


@admin.register(User)
class UserAdmin(DisplayEmptyFielsdMixin, admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'role', 'bio',)
    search_fields = ('username', 'email', 'role',)
    list_filter = ('role',)


@admin.register(Review)
class ReviewAdmin(DisplayEmptyFielsdMixin, admin.ModelAdmin):
    list_display = ('pk', 'pub_date', 'author', 'text', 'title', 'score',)
    search_fields = ('text', 'author__username',)
    list_filter = ('score', 'pub_date',)


@admin.register(Comment)
class CommentAdmin(DisplayEmptyFielsdMixin, admin.ModelAdmin):
    list_display = ('pk', 'review', 'pub_date', 'author', 'text',)
    search_fields = ('text', 'author__username',)
    list_filter = ('pub_date',)


@admin.register(Category)
class CategoryAdmin(DisplayEmptyFielsdMixin, admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Genre)
class GenreAdmin(DisplayEmptyFielsdMixin, admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Title)
class TitleAdmin(DisplayEmptyFielsdMixin, admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category', 'description',)
    list_editable = ('category',)
    search_fields = ('name',)
    list_filter = ('year',)
