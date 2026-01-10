from django.contrib import admin
from .models import Competence, Education, Experience, Project, Message, Information, TypingText

@admin.register(Information)
class InformationAdmin(admin.ModelAdmin):
    pass

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    pass

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    pass

@admin.register(Competence)
class CompetenceAdmin(admin.ModelAdmin):
    pass

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass

@admin.register(TypingText)
class TypingTextAdmin(admin.ModelAdmin):
    list_display = ('text', 'created_at')