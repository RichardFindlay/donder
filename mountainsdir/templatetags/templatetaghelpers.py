from django import template
from django.template.defaultfilters import timesince
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from user_accounts.models import PostImage, userProfile, JournalEntry

register = template.Library()

@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = f'?{field_name}={value}'
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = f'{url}&{encoded_querystring}'
    return url

@register.filter(name='split')
def split(value, arg):
    return value.split(arg)

@register.filter(name='return_item')
def return_item(l, i):
    try:
        return l[i]
    except:
        return None
    

@register.filter(name='addpercent')
def addpercent(value):
    return str(value) + "%"


@register.filter(name='returnlatitude')
def returnlatitude(value, arg):
    # value is the moutain obj & arg is mountain name
    obj = value.filter(name=arg)

    latitude = obj.values_list("latitude", flat=True)[0]
    # longitude = obj.values_list("latitude", flat=True)[0]

    return latitude


@register.filter(name='returnlongitude')
def returnlongitude(value, arg):
    # value is the moutain obj & arg is mountain name
    obj = value.filter(name=arg)

    longitude = obj.values_list("longitude", flat=True)[0]
    # longitude = obj.values_list("latitude", flat=True)[0]

    return longitude


@register.filter(name='totalascents')
def totalascents(value, arg):
    # value is the moutain obj & arg is mountain name
    mountain = value.filter(name=arg)

    ascents = mountain.values_list("ascend_count", flat=True)[0]

    return ascents

@register.filter(name='getheight')
def getheight(value, arg):
    # value is the moutain obj & arg is mountain name
    mountain = value.filter(name=arg)

    height = mountain.values_list("height_meters", flat=True)[0]

    return height

@register.filter(name='get_location_region')
def get_location_area(value, arg):
    # value is the moutain obj & arg is mountain name
    mountain = value.filter(name=arg)

    region = mountain.values_list("region", flat=True)[0]

    # remove intial code from string
    region = region[5:]

    return region



@register.filter(name='returnclassifications')
def returnclassifications(value, arg):
    # value is the moutain obj & arg is mountain name
    obj = value.filter(name=arg)

    classes = obj.values_list("classification", flat=True)[0]

    return classes


@register.filter(name='filterpostimages')
def filterpostimages(value, journal_obj):
    # value is the post obj & arg is journal id
    images = value.filter(post=journal_obj)

    return images

@register.filter(name='time_since_last_update')
def time_since_last_update(date):
    """
    Returns the time since a post was last updated.
    """
    time_diff = timezone.now() - date

    if time_diff < timedelta(days=1):

        # Format the time difference in seconds or hours
        if time_diff < timedelta(seconds=60):
            time_since = f"{time_diff.seconds}s"
        elif time_diff > timedelta(seconds=60) and time_diff < timedelta(hours=1):
            minutes = round(time_diff.seconds % 3600 / 60)
            time_since = f"{ minutes } min{'s' if minutes > 1 else ''}"
        else:
            hours = int(time_diff.total_seconds() / 3600)
            time_since = f"{hours} hr{'s' if hours > 1 else ''}"
    else:
        # Round to the nearest day
        time_diff = round(time_diff.days) * timedelta(days=1)
        # Format the time difference in days
        days = int(time_diff.total_seconds() / 86400)
        time_since = f"{days} day{'s' if days > 1 else ''}"


    return time_since


@register.filter(name='get_ascend_count')
def get_ascend_count(value, name):

    count = value.get(name=name)
    
    return count.ascent_count



@register.filter(name='get_full_name_user')
def get_full_name_user(value):
    # value is the moutain obj & arg is mountain name
    user_obj = User.objects.get(username=value)

    fistname = user_obj.first_name 
    lastname = user_obj.last_name

    return fistname + ' ' + lastname


@register.filter(name='get_user_location')
def get_user_location(value):

    current_user = userProfile.objects.get(user=value)
    
    return current_user.location


@register.filter(name='get_user_city')
def get_user_city(value):

    current_user = userProfile.objects.get(user=value)
    
    return current_user.town_city





@register.filter(name='get_user_profile_image')
def get_user_profile_image(value):
    # value is the moutain obj & arg is mountain name
    user_obj = User.objects.get(username=value)
    profile_obj = userProfile.objects.get(user=user_obj)

    return profile_obj.profileimg.url


@register.filter(name='time_lapsed_seconds')
def time_lapsed_seconds(date):

    time_diff = timezone.now() - date

    return int(time_diff.seconds)


@register.filter(name='filter_for_current_mountain')
def filter_for_current_mountain(value, mountain_name):

    filtered = value.filter(mountain_name=mountain_name)
    # filtered = filtered.order_by('-created_at')

    if filtered.count() != 0:
        return filtered
    else:
        return [''] # return array to ensure reaches condition statement



@register.filter(name='post_image_thumbnail')
def post_image_thumbnail(value):
    # get post for current post
    current_post = JournalEntry.objects.filter(id=value).first()

    if current_post:
        # get images for current post
        post_images = PostImage.objects.filter(post=current_post)

        if post_images.exists():
            # just get the first image if present
            post_img = post_images.first().image.url
            print('------------------')
            print(post_img)
        else:
            post_img = False
    else:
        post_img = False

    return post_img


@register.filter(name='replace_spaces')
def replace_spaces(value):
    return value.replace(' ', '_')