from django.urls import path
from .views import capture_butterfly, butterfly_list, signup

urlpatterns = [
    path('', butterfly_list, name='butterfly_list'),  # List of captured butterflies
    path('capture/', capture_butterfly, name='capture_butterfly'),  # Capture form
    path('signup/', signup, name='signup'),  # Signup for researchers only
]
