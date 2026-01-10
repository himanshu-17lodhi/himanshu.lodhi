from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q
from decouple import config
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib import messages
from info.forms import MessageForm
from info.models import (
    Competence,
    Education,
    Experience,
    Project,
    Information,
    Message,
    TypingText
)
import logging
import json


logger = logging.getLogger(__name__)

def email_send(data):
    email = EmailMessage(
        subject=f'Portfolio : Mail from {data.get("name")}',
        body=data.get("message"),
        from_email=settings.EMAIL_HOST_USER,
        to=[settings.EMAIL_HOST_USER],
        reply_to=[data.get("email")],
    )
    try:
        email.send()
        return True
    except Exception as e:
        logger.error(f"Email error: {e}")
        return False

def homePage(request):
    template_name = 'homePage.html'
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            data = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message']
            }
            if email_send(data):
                form.save()
                messages.success(request, "Your message has been sent successfully!")
            else:
                form.save()
                messages.warning(request, "Message saved, but there was an issue sending the email notification.")
            
            return redirect('/#message-me')
        else:
            messages.error(request, "Please correct the errors in the form.")
            return redirect('/#message-me')

    form = MessageForm()
    competences = Competence.objects.all().order_by('id')
    education = Education.objects.all().order_by('-id')
    experiences = Experience.objects.all().order_by('-id')
    projects = Project.objects.filter(show_in_slider=True).order_by('-id')
    info = Information.objects.first()
    typing_words = list(TypingText.objects.values_list('text', flat=True))

    context = {
        'info': info,
        'typing_words': typing_words,
        'competences': competences,
        'education': education,
        'experiences': experiences,
        'projects': projects,
        'form': form,
    }
    
    return render(request, template_name, context)

def projectsPage(request):
    template_name = 'projects/projects_page.html'
    if request.method == 'GET':
        projects = Project.objects.all().order_by('-id')
        context = {'projects': projects}
        return render(request, template_name, context)

def projectDetail(request, slug):
    template_name = 'projects/project_detail.html'
    if request.method == 'GET':
        project = get_object_or_404(Project, slug=slug)
        return render(request, template_name, {'project': project})
        
def search(request):
    if request.method == 'POST':
        search_text = request.POST.get('searchText', False)
        if search_text:
            lookups = Q(title__icontains=search_text) | Q(
                description__icontains=search_text) | Q(tools__icontains=search_text)

            objs = Project.objects.filter(lookups)
            if objs:
                projects = Project.objects.filter(lookups).values()
                projects = list(projects)
                for project, obj in zip(projects, objs):
                    project.update({
                        'url': obj.get_project_absolute_url(),
                        'image_url': obj.image.url
                    })
                return JsonResponse({'success': True, 'projects': projects, 'searchText': search_text})
    return JsonResponse({'success': False, 'searchText': search_text})

def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)

def test404(request):
    return render(request, 'errors/404.html')
