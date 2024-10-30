"""
URL configuration for RealEstateListings project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from RealEstateListings import settings
from users.views import custom_404_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Homeapp.urls')),#Home app based on site visitor
    path('adminpanel/', include('adminpanel.urls')),  # Admin panel URLs
    path('Agent/', include('Agent.urls')),  # agnt,include(Contact,notification) URLs
    path('users/', include('users.urls')),  # User-related URLs (registration, login, profiles)
    
]
if settings.DEBUG:  # Only serve files this way in development
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   
