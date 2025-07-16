from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='advertisers'),
  path('newadvertiser/', views.createAdvertiser, name='createAdvertiser'),
  path('<int:advertiser_id>', views.advertiser, name='advertiser'),
]