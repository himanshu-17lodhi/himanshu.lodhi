import os
import re
from django.db import models
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field
from django.core.exceptions import ValidationError

class Information(models.Model):
    name_complete = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatar/", blank=True, null=True)
    mini_about = models.TextField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    born_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    cv = models.FileField(upload_to='cv', blank=True, null=True)

    # Social Network
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name_complete

def validate_image_file_extension(value):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg']
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed: jpg, jpeg, png, gif, svg.')

def competence_image_choices():
    """
    Returns a list of tuples for available images in static/competence/.
    """
    static_folder = os.path.join(settings.BASE_DIR, 'static', 'competence')
    try:
        files = [
            (f'competence/{f}', f)
            for f in os.listdir(static_folder)
            if os.path.isfile(os.path.join(static_folder, f))
        ]
    except FileNotFoundError:
        files = []
    return files

class Competence(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    image_from_static = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        choices=competence_image_choices(),
        verbose_name="Select image from static/competence/"
    )

    def __str__(self):
        return self.title

    # In your template, use: {% load static %} <img src="{% static competence.image_from_static %}" alt="{{ competence.title }}">
    # There is no need for a get_image_url method.

class Education(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    the_year = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.title

class Experience(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    the_year = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.title

class Project(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    description = CKEditor5Field(blank=False, null=False)
    image = models.ImageField(upload_to="projects/", blank=False, null=False)
    tools = models.CharField(max_length=200, blank=False, null=False)
    demo = models.URLField()
    github = models.URLField()
    show_in_slider = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_project_absolute_url(self):
        return "/projects/{}".format(self.slug)

    def save(self, *args, **kwargs):
        self.slug = self.slug_generate()
        super(Project, self).save(*args, **kwargs)

    def slug_generate(self):
        slug = self.title.strip()
        slug = re.sub(" ", "_", slug)
        return slug.lower()

class Message(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=255, null=False, blank=False)
    message = models.TextField(null=False, blank=False)
    send_time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.name
