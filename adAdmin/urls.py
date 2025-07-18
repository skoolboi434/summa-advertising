from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='adminPortal'),
  path('admingeneral', views.adminGeneral, name='adminGeneral'),
]