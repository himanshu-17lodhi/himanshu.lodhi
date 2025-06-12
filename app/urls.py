from django.contrib import admin
from django.urls import path, include
from .views import (
    homePage,
    projectsPage,
    projectDetail,
    search,
    handler404,
)

from django.conf import settings
from django.conf.urls.static import static

handler404 = handler404

urlpatterns = [
    path(settings.DJANGO_ADMIN_URL, admin.site.urls),
    path('', homePage, name='homePage'),
    path('projects/', projectsPage, name='projectsPage'),
    path('projects/<str:slug>/', projectDetail, name='projectDetail'),
    path('search/', search, name='search'),
    path('dashboard/', include('dashboard.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)