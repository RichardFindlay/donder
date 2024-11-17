from django.contrib import admin
from .models import userProfile, JournalEntry, PostImage, StripeUser

# Register your models here.
admin.site.register(userProfile)
admin.site.register(JournalEntry)
admin.site.register(PostImage)
admin.site.register(StripeUser)