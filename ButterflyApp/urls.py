from django.urls import path
from .views import capture_butterfly, butterfly_list

urlpatterns = [
    path('capture/', capture_butterfly, name='home'),
    path('', butterfly_list, name='butterfly_list'),
]
