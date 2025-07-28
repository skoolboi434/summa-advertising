from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='adminPortal'),
  path('admingeneral', views.adminGeneral, name='adminGeneral'),
  path('adminaccounts', views.adminAccounts, name='adminAccounts'),
  path('admingeneral/newpublication/', views.adminPubSetup, name='adminPubSetup'),
  path('newuser/', views.createUser, name='createUser'),
  
]