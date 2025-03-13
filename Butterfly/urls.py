from django.contrib import admin
from django.urls import include, path

from django.conf import settings                    # ✅ Import settings
from django.conf.urls.static import static          # ✅ Import static

from ButterflyApp.views import custom_login

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Redirect root URL to the login page
    path('', custom_login, name="home"),

    # Researcher (Regular User) URLs
    path('butterflies/', include('ButterflyApp.urls')),

    # Expert URLs (Separate for expert role)
    path('experts/', include('ButterflyApp.experts_urls')),

    # Authentication URLs (Login, Logout, Password Reset, etc.)
    path('accounts/login/', custom_login, name="login"),
    path('accounts/', include('django.contrib.auth.urls')),
]

# ✅ Serve media files during development
if settings.DEBUG:   # Only serve media in debug mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
