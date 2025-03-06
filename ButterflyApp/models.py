from django.db import models


class Butterfly(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="butterflies/")
    date_taken = models.DateTimeField(auto_now_add=True)
    characteristics = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.date_taken.strftime('%Y-%m-%d %H:%M')}"
