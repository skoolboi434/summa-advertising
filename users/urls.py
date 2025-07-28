from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='users'),
  path('<int:id>', views.userProfile, name='userProfile'),
]