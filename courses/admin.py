from django.contrib import admin

from .models import (Course, Enrollment, Announcement, Comment,
Lesson, Material)


class CourseAdmin(admin.ModelAdmin): #serve para personalizar o admin
    list_display = ['name', 'slug', 'start_date', 'created_at']
    search_fields = ['name', 'slug'] #campos que estarão disponiveis p busca
    prepopulated_fields = {'slug': ('name',)}#faz o atalho automatico, só vale para os novos

class MaterialInlineAdmin(admin.StackedInline):

    model = Material

class LessonAdmin(admin.ModelAdmin):
    list_display = ['name', 'number', 'course', 'release_date']
    search_fields = ['name', 'description']
    list_filter = ['created_at']#filtragem lateral
    #
    inlines = [MaterialInlineAdmin]

admin.site.register(Course, CourseAdmin)
admin.site.register([Enrollment, Announcement, Comment])
admin.site.register(Lesson, LessonAdmin)