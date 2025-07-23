from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='advertisers'),
  path('newadvertiser/', views.createAdvertiser, name='createAdvertiser'),
  path('<int:id>', views.advertiser, name='advertiser'),
  path('<int:id>/add-contact/', views.add_contact, name='add_contact'),
  path('<int:id>/add-notes/', views.add_notes_to_advertiser, name='add_advertiser_notes')

]