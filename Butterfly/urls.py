"""
URL configuration for Butterfly project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include, path
from ButterflyApp.views import custom_login
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Redirect root URL to the login page
    path("", custom_login, name="home"),

    # Researcher (Regular User) URLs
    path("butterflies/", include("ButterflyApp.urls")),

    # Expert URLs (Separate for expert role)
    path("experts/", include("ButterflyApp.experts_urls")),

    # Authentication URLs (Login, Logout, Password Reset, etc.)
    path("accounts/login/", custom_login, name="login"),
    path("accounts/", include("django.contrib.auth.urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

