from django.contrib import admin

from .models import Course, Enrollment, Announcement, Comment

class CourseAdmin(admin.ModelAdmin): #serve para personalizar o admin
    list_display = ['name', 'slug', 'start_date', 'created_at']
    search_fields = ['name', 'slug'] #campos que estarão disponiveis p busca
    prepopulated_fields = {'slug': ('name',)}#faz o atalho automatico, só vale para os novos

admin.site.register(Course, CourseAdmin)
admin.site.register([Enrollment, Announcement, Comment])