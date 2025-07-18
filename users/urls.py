from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='users'),
  path('<int:user_id>', views.userProfile, name='userProfile'),
]