from django.contrib import admin
from django.urls import path, include
import pages.urls
import adCampaigns.urls
import advertisers.urls
import users.urls
import adAdmin.urls
import classifieds.urls



urlpatterns = [
    path('', include(pages.urls)),
    path('adcampaigns/', include(adCampaigns.urls)),
    path('advertisers/', include(advertisers.urls)),
    path('users/', include(users.urls)),
    path('adminportal/', include(adAdmin.urls)),
    path('classifieds/', include(classifieds.urls)),
    path('admin/', admin.site.urls),
]
