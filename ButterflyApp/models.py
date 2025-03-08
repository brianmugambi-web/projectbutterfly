from django.db import models

class Butterfly(models.Model):
    name = models.CharField(max_length=255)
    species = models.CharField(max_length=255, blank=True, null=True)
    characteristics = models.TextField()
    image = models.ImageField(upload_to="butterflies/images/", blank=True, null=True)
    video = models.FileField(upload_to="butterflies/videos/", blank=True, null=True)
    date_taken = models.DateTimeField(auto_now_add=True)

    # New fields for location
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    location_name = models.CharField(max_length=500, blank=True, null=True)  # Store full address

    def __str__(self):
        return f"{self.name} - {self.location_name}"
