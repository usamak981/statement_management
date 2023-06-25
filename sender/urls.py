from django.urls import path
from sender import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    # Other URL patterns
    path('list/', login_required(views.sender_list), name='sender_list'),
    path('create/', login_required(views.sender_create), name='sender_create'),
    path('<int:pk>/update/', login_required(views.sender_update), name='sender_update'),
    path('<int:pk>/delete/', login_required(views.sender_delete), name='sender_delete'),
]
