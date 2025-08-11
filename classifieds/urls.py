from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='classifieds'),
  path('newClassified/', views.createClassified, name='createClassified'),
]