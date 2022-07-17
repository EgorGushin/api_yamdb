from django.contrib import admin


class DisplayEmptyFielsdMixin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
