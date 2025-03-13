from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings

from django.utils import timezone



class CustomUser(AbstractUser):  # Unified user model
    email = models.EmailField(unique=True)
    is_researcher = models.BooleanField(default=True)  # Default user is a researcher
    is_expert = models.BooleanField(default=False)  # Admin must set this manually

    groups = models.ManyToManyField(Group, related_name="custom_users", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_permissions", blank=True)

    def __str__(self):
        return f"{self.username} ({'Expert' if self.is_expert else 'Researcher'})"





class Butterfly(models.Model):
    name = models.CharField(max_length=255)
    species = models.CharField(max_length=255, blank=True, null=True)
    characteristics = models.TextField()

    # Optional fields for single media
    image = models.ImageField(upload_to="butterflies/images/", blank=True, null=True)
    video = models.FileField(upload_to="butterflies/videos/", blank=True, null=True)

    date_taken = models.DateTimeField(auto_now_add=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    location_name = models.CharField(max_length=500, blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("validated", "Validated"), ("rejected", "Rejected")],
        default="pending"
    )

    # ✅ Fixed researcher relation
    researcher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='butterflies'
    )

    def __str__(self):
        return f"{self.name} - {self.location_name or 'Unknown Location'} - {self.date_taken.strftime('%Y-%m-%d %H:%M')}"


class ButterflyMedia(models.Model):
    MEDIA_TYPE_CHOICES = [
        ("image", "Image"),
        ("video", "Video"),
    ]

    butterfly = models.ForeignKey(Butterfly, on_delete=models.CASCADE, related_name='media')
    media_file = models.FileField(upload_to="butterflies/media/")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    # ✅ Fixed researcher relation
    researcher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='butterfly_media'
    )

    def __str__(self):
        return f"{self.media_type.capitalize()} for {self.butterfly.name}"


    
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

