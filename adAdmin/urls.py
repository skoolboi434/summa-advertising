from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='adminPortal'),
  path('admingeneral', views.adminGeneral, name='adminGeneral'),
  path('adminAds', views.adminAds, name='adminAds'),
  path('adminclassifieds', views.adminClassifieds, name='adminClassifieds'),
  path('adminaccounts', views.adminAccounts, name='adminAccounts'),
  path('adminFinancial', views.adminFinancial, name='adminFinancial'),
  path('admingeneral/newpublication/', views.adminPubSetup, name='adminPubSetup'),
  path('new-user/', views.createUser, name='createUser'),
  path('new-style/', views.createAdminStyle, name='createAdminStyle'),
  
]