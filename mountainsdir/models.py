from django.db import models
import uuid

# main hills/mountains class.
class mountain(models.Model):
    # mountain_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    classification_orig = models.CharField(max_length=255)
    classification = models.CharField(max_length=255)
    height_meters = models.FloatField(default=0)
    height_feet = models.FloatField(default=0)
    grid_ref = models.CharField(max_length=255)
    feature = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    country_abbr = models.CharField(max_length=255)
    ascend_count = models.IntegerField(default=0)
    # img = models.ImageField(upload_to='images/', default=None)



