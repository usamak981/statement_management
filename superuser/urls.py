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
from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('event_managers/list/', login_required(list_event_managers), name='list_event_managers'),
    path('event_managers/create/', login_required(create_event_manager), name='create_event_manager'),
    path('event_managers/<int:id>/delete/', login_required(delete_event_manager), name='delete_event_manager'),


    path('event_categorys/list/', login_required(event_category_list), name='event_category_list'),
    path('event_categorys/create/', login_required(create_event_category), name='create_event_category'),
    path('event_categorys/<int:id>/edit/', login_required(edit_event_category), name='edit_event_category'),
    path('event_categorys/<int:id>/delete/', login_required(delete_event_category), name='delete_event_category'),


    path('events/list/', login_required(event_list), name='event_list'),
    path('events/create/', login_required(create_event), name='create_event'),
    path('events/<int:id>/edit/', login_required(edit_event), name='edit_event'),
    path('events/<int:id>/delete/', login_required(delete_event), name='delete_event'),


    path('event_participant/<int:id>/list/', login_required(event_participant), name='event_participant'),
    path('event_participant/list/', login_required(user_created_participant), name='user_created_participant'),
    path('event_participant/create/', login_required(create_event_participant), name='create_event_participant'),
    path('event_participant/<int:id>/delete', login_required(delete_event_participant), name='delete_event_participant'),
    path('event_participant/<int:id>/edit', login_required(edit_event_participant), name='edit_event_participant'),


    path('event_certificates/list/', login_required(event_certificates), name='event_certificates'),
    path('generate_bulk_certificate/<int:event_id>/<int:id>/', login_required(generate_bulk_certificate), name='generate_bulk_certificate'),
    # path('event_certificates/create/', login_required(create_event_certificate), name='create_event_certificate'),
    # path('event_certificates/<int:id>/edit/', login_required(edit_event_certificate), name='edit_event_certificate'),
    path('event_certificates/<int:id>/delete/', login_required(delete_event_certificate),
         name='delete_event_certificate'),


    path('quiz/list/', login_required(all_user_quiz), name='quiz'),
    path('quiz/create/', login_required(create_quiz), name='create_quiz'),
    path('quiz/<int:id>/edit/', login_required(edit_quiz), name='edit_quiz'),
    path('quiz/<int:id>/delete/', login_required(delete_quiz), name='delete_quiz'),

    path('questions/<int:quiz_id>/list/', login_required(quiz_questions), name='quiz_questions'),
    path('questions/<int:quiz_id>/create/', login_required(add_quiz_questions), name='add_quiz_questions'),
    path('questions/<int:id>/edit/', login_required(edit_question), name='edit_question'),
    path('questions/<int:id>/delete/', login_required(delete_question), name='delete_quiz_question'),

    path('answers/<int:question_id>/list/', login_required(answers_of_question), name='answers_of_question'),
    path('answers/<int:question_id>/create/', login_required(add_answers_to_question), name='add_answers_to_question'),
    path('answers/<int:id>/edit/', login_required(edit_answer), name='edit_answer'),
    path('answers/<int:id>/mark_answer_as_correct/', login_required(mark_answer_as_correct), name='mark_answer_as_correct'),
    path('answers/<int:id>/delete/', login_required(delete_answer), name='delete_answer'),

]
