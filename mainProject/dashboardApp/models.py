from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    POSITION_CHOICES = [
        ("Staff", "Staff"),
        ("Administrator", "Administrator"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    pf_picture = models.ImageField(null=True, blank=True, upload_to="images/", default="images/default.jpg",)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, default="Staff")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return self.user.username