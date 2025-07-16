from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='adCampaigns'),
  path('newcampaign/', views.createCampaign, name='createCampaign'),
  path('newad/', views.createAd, name='createAd'),
  path('<int:campaign_id>', views.adCampaign, name='adCampaign'),
]