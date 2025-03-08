from django.urls import path
from .views import review_butterfly, expert_dashboard  # Ensure correct view imports

urlpatterns = [
    path('dashboard/', expert_dashboard, name='expert_dashboard'),  # Experts' home
    path('review/<int:record_id>/', review_butterfly, name='review_butterfly'),  # Reviewing submissions
]
