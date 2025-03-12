from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models



class CustomUser(AbstractUser):  # Unified user model
    email = models.EmailField(unique=True)
    is_researcher = models.BooleanField(default=True)  # Default user is a researcher
    is_expert = models.BooleanField(default=False)  # Admin must set this manually

    groups = models.ManyToManyField(Group, related_name="custom_users", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_permissions", blank=True)

    def __str__(self):
        return f"{self.username} ({'Expert' if self.is_expert else 'Researcher'})"

class Butterfly(models.Model):
    name = models.CharField(max_length=255)  # Increased to match Kray's version
    species = models.CharField(max_length=255, blank=True, null=True)  # Increased for consistency
    characteristics = models.TextField()
    image = models.ImageField(upload_to="butterflies/images/", blank=True, null=True)
    video = models.FileField(upload_to="butterflies/videos/", blank=True, null=True)
    date_taken = models.DateTimeField(auto_now_add=True)
    
    # Location tracking fields (from Kray's implementation)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    location_name = models.CharField(max_length=500, blank=True, null=True)

    # Status tracking for expert validation
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("validated", "Validated"), ("rejected", "Rejected")],
        default="pending"
    )

    def __str__(self):
        return f"{self.name} - {self.location_name if self.location_name else 'Unknown Location'} - {self.date_taken.strftime('%Y-%m-%d %H:%M')}"
    
class ExpertReview(models.Model):
    butterfly = models.ForeignKey(Butterfly, on_delete=models.CASCADE)
    expert = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_expert': True})
    feedback = models.TextField()
    species_identification = models.CharField(max_length=255, blank=True, null=True)
    review_date = models.DateTimeField(auto_now_add=True)
    decision = models.CharField(  # Field for expert decision
        max_length=10,
        choices=[("accept", "Accept"), ("reject", "Reject")],
        default="reject"
    )

    def __str__(self):
        return f"Review by {self.expert.username} on {self.butterfly.name} - {self.decision}"

