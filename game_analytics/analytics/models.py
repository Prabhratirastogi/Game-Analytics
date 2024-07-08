from django.db import models

# Create your models here.
# analytics/models.py

class Game(models.Model):
    app_id = models.IntegerField(unique=True)  # Changed field name from app_id to app_id for consistency
    name = models.CharField(max_length=255)
    release_date = models.DateField()
    required_age = models.IntegerField(null=True, blank=True)  # Make required_age nullable
    price = models.FloatField(null=True, blank=True)  # Make price nullable
    dlc_count = models.IntegerField(null=True, blank=True)  # Make dlc_count nullable
    about_the_game = models.TextField(null=True, blank=True)  # Make about_the_game nullable
    supported_languages = models.JSONField(null=True, blank=True)  # Make supported_languages nullable
    windows = models.BooleanField(default=False)  # Set default value for windows
    mac = models.BooleanField(default=False)  # Set default value for mac
    linux = models.BooleanField(default=False)  # Set default value for linux
    positive_reviews = models.IntegerField(default=0)  # Set default value for positive_reviews
    negative_reviews = models.IntegerField(default=0)  # Set default value for negative_reviews
    score_rank = models.IntegerField(null=True, blank=True)  # Make score_rank nullable
    developers = models.CharField(max_length=255, null=True, blank=True)  # Make developers nullable
    publishers = models.CharField(max_length=255, null=True, blank=True)  # Make publishers nullable
    categories = models.CharField(max_length=255, null=True, blank=True)  # Make categories nullable
    genres = models.CharField(max_length=255, null=True, blank=True)  # Make genres nullable
    tags = models.CharField(max_length=255, null=True, blank=True)  # Make tags nullable
    
    def __str__(self):
        return f"{self.name} (AppID: {self.app_id}, Release Date: {self.release_date})"
