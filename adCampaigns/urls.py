from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='adCampaigns'),
  path('newcampaign/', views.createCampaign, name='createCampaign'),
  path('ads', views.allAds, name='allAds'),
  path('newad/', views.createAd, name='createAd'),
  path('<int:id>', views.adCampaign, name='adCampaign'),
  path('advertiser-search/', views.advertiser_search, name='advertiser_search'),
  path('ads/<int:ad_id>', views.singleAd, name='singleAd'),
]