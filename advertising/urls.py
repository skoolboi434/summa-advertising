from django.contrib import admin
from django.urls import path, include
import pages.urls
import adCampaigns.urls

urlpatterns = [
    path('', include(pages.urls)),
    path('adcampaigns/', include(adCampaigns.urls)),
    path('admin/', admin.site.urls),
]
