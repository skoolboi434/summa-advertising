from django.contrib import admin
from django.urls import path, include
import pages.urls
import adCampaigns.urls
import advertisers.urls

urlpatterns = [
    path('', include(pages.urls)),
    path('adcampaigns/', include(adCampaigns.urls)),
    path('advertisers/', include(advertisers.urls)),
    path('admin/', admin.site.urls),
]
