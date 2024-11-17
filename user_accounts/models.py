from django.db import models
from django.contrib.auth import get_user_model
from mountainsdir.models import mountain
import uuid
from datetime import datetime
import pytz

User = get_user_model()

# helper function to 
def profile_pictures_ids(instance, filename):
    return f'media/profile_images/{str(instance.id_user)}_{str(instance.user.first_name)}_{str(instance.user.last_name)}/{filename}'


# Create your models here.
class userProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to=profile_pictures_ids, default='default_profile_photo.jpg')
    location = models.CharField(max_length=100, blank=True, null=True)
    town_city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

def id2str(instance):
    return str(instance.JournalEntry.id)
    
class JournalEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    id_str = models.CharField(max_length=64, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images', blank=True)
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    mountain_name = models.TextField(blank=True)
    date_climbed = models.DateTimeField(default=datetime.now, blank=True)
    mountain_fk = models.ForeignKey(mountain, on_delete=models.CASCADE, related_name='journal_entries', null=True, blank=True)

    def __str__(self):
        return self.user.username

def picture_ids(instance, filename):
    return f'media/post_images/{str(instance.post.id)}/{filename}'



# post images has seperate model to allow for multiple uploads:
class PostImage(models.Model):
    post = models.ForeignKey(JournalEntry, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=picture_ids)


class StripeUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=255, blank=True, null=True, default=False)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True, default=False)
    is_paid = models.BooleanField(default=False)
    price = models.FloatField(default=0.0, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True, default=False)
    plan = models.CharField(max_length=15, blank=True, null=True, default=False)
    stripe_product = models.CharField(max_length=255, blank=True, null=True, default=False)
    recurring_interval = models.CharField(max_length=255, blank=True, null=True, default=False)
    created_at = models.DateTimeField(default=datetime.now)
    end_date_of_subscription = models.DateTimeField(default=datetime.now)

    # def active_subscription(self):
    #     if self.end_date_of_subscription:
    #         return datetime.now(pytz.utc) < self.end_date_of_subscription
    #     else:  
    #         return True

    def active_subscription(self):
        if self.is_paid:
            return True
        else:  
            return False



    def __str__(self):
        return f"{self.user.username} {self.plan}"

