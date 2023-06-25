"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include, re_path

# --Static file Configurations-----------------
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView
from superuser.views import certificate_for_participant, preview_certificate, quiz_attempt_form
from accounts.views import *
from managers import views

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('login'), permanent=True)),
    path('events/<int:event_id>/certificate_for_participant/', certificate_for_participant,
         name='certificate_for_participant'),
    path('preview_certificate/<int:id>/', preview_certificate, name='preview_certificate'),
    path('quiz/<int:quiz_id>/quiz_attempt/', quiz_attempt_form, name='quiz_attempt_form'),

    path('error_page/', error_page, name="error_page"),
    path('accounts/', include('accounts.urls')),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', include('superuser.urls')),
    path('admin/', include('managers.urls')),
    path('senders/', include('sender.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
