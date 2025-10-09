from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='adminPortal'),
  path('admingeneral', views.adminGeneral, name='adminGeneral'),
  path('adminAds', views.adminAds, name='adminAds'),
  path('adminclassifieds', views.adminClassifieds, name='adminClassifieds'),
  path('adminaccounts', views.adminAccounts, name='adminAccounts'),
  path('adminFinancial', views.adminFinancial, name='adminFinancial'),
  path('adminPricing', views.adminPricing, name='adminPricing'),
  path('admingeneral/newpublication/', views.adminPubSetup, name='adminPubSetup'),
  path('new-user/', views.createUser, name='createUser'),
  path('new-style/', views.createAdminStyle, name='createAdminStyle'),
  path('admingeneral/new-magazine/', views.newMagazine, name='newMagazine'),
  path('admingeneral/new-newspaper/', views.newNewspaper, name='newNewspaper'),
  path('admingeneral/new-digital/', views.newDigital, name='newDigital'),

  path('publication/<int:pk>/', views.publication_dashboard, name='publication-dashboard'),


  
  path("advertising/json/add/standardsize/", views.add_standardsize, name="add_standardsize"),

  path('rate-groups/<int:id>/', views.singleRateGroup, name='singleRateGroup'),
  
]