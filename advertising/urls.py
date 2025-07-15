from django.contrib import admin
from django.urls import path, include
import pages.urls

urlpatterns = [
    path('', include(pages.urls)),
    path('admin/', admin.site.urls),
]
