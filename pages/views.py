from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from mountainsdir.models import mountain
from user_accounts.models import userProfile, JournalEntry, PostImage, StripeUser
from django.urls import reverse
from django.core.paginator import Paginator
from user_accounts.forms import NewUserForm
# from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncDay
from django.db.models import Count, Sum, Value
from django.conf import settings
from datetime import datetime, timedelta
from collections import OrderedDict
from django.template.defaultfilters import timesince
import numpy as np
from django.template.defaultfilters import timesince
from django.utils.timezone import localtime, now
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Case, When, Subquery, OuterRef, IntegerField, Prefetch
import os
import stripe
import json
import logging
from mountainsdir.forms import MountainSearchForm
from environ import Env 
from pathlib import Path

env = Env()
env_path = Path('../donder/.env')  # Replace with your .env file's path
env.read_env(env_path)


# Configure the logger
logger = logging.getLogger(__name__)

# declare category list;
cat_list = {
        'M':    'Munro',
        'Dew':	'Dewey',
        'W':	'Wainwright',
        'C':	'Corbett',
        'F':	'Furth',
        'G':	'Graham',
        'Dew':	'Donald',
        'VL':	'Vandeleur-Lynam',
        'A':	'Arderin',
        'Ma':	'Marilyn',
        'Hu':	'Hump',
        'Tu':	'Tump',
        'Sim':	'Simm',
        '5':	'Dodd',
        'Hew':	'Hewitt',
        'B':	'Birkett',
        'N':	'Nuttall'
    }


'''
country codes:
'S' - Scotland = "SCO"
'C' - Channel Islands = "CHI"
'E' - England = "ENG"
'ES' - Northumberland/Scottish Borders = "ENG"
'M' - Isle of Man = "IM"
'W' - Wales = "WLS"
'I' - Ireland = "IRE"
'''

print('HERE_HERE_HERE')

# @login_required(login_url='home')
def user_profile(request, *args, **kwargs):
    user_obj = User.objects.get(username=request.user.username)
    user_profile = userProfile(user=user_obj)
    return user_profile

# Create your views here.
def landing_page(request, *args, **kwargs):
    # set default data
    mountainlist = mountain.objects.all()
    filter_by = request.GET.get('filter_by', 'all')
    order_by = request.GET.get('order_by', 'ascents')
    class_type = request.GET.get('class_type')
    time_period = request.GET.get('time_period', 'all_time')
    grid_map = request.GET.get('grid_map', 'grid_view')
    context = {}

    if request.method == "POST":
        email = request.POST['login-email']
        password = request.POST['login-password']

        user = auth.authenticate(username=email, password=password)

        if user is not None:
            auth.login(request, user)

            user = User.objects.get(username=request.user.username)
            user_profile_obj = userProfile.objects.get(user=user)

            first_name = user.first_name
            last_name = user.last_name

            id_user = user_profile_obj.id_user
            
            url = reverse('profile_dashboard', kwargs={'first_name': first_name.lower(), 'last_name': last_name.lower(), 'id_user': id_user})

            return redirect(url)
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('home') # additional logic implemented into login modal to prompt reload if error

    if filter_by == 'all':
        mountainlist = mountain.objects.all()
    elif filter_by == 'scotland':
        mountainlist = mountain.objects.filter(country='S')
    elif filter_by == 'ireland':
        mountainlist = mountain.objects.filter(country='I')
    elif filter_by == 'england':
        mountainlist = mountain.objects.filter(country='E')
    elif filter_by == 'wales':
        mountainlist = mountain.objects.filter(country='W')

    if class_type:
        mountainlist = mountainlist.filter(classification__contains=class_type)

    # filtered journal entry objects
    filtered_names = mountainlist.values_list('name', flat=True)
    filter_journals = JournalEntry.objects.filter(mountain_fk__name__in=filtered_names)

    # now filter journal entries to get ascent counts
    todays_date = datetime.today()
    if time_period == "last_24hrs":
        yesterday = todays_date - timedelta(days=1)
        filtered_journals = filter_journals.filter(date_climbed__range=[yesterday.strftime('%Y-%m-%d'), todays_date.strftime('%Y-%m-%d')])
    if time_period == "this_week":
        first_day_of_week = todays_date - timedelta(days=todays_date.weekday())
        filtered_journals = filter_journals.filter(date_climbed__range=[first_day_of_week.strftime('%Y-%m-%d'), todays_date.strftime('%Y-%m-%d')])
    elif time_period == "this_month":
        filtered_journals = filter_journals.filter(date_climbed__range=[f"{todays_date.year}-{todays_date.month}-01", todays_date.strftime('%Y-%m-%d')])
    elif time_period == "this_year":
        filtered_journals = filter_journals.filter(date_climbed__range=[f"{todays_date.year}-01-01", todays_date.strftime('%Y-%m-%d')])
    elif time_period == "all_time":
        filtered_journals = filter_journals 
    

    # annotate each mountain with the ascent count for that mountain
    mountainlist = mountainlist.annotate(
        ascent_count=Count('journal_entries', filter=Q(journal_entries__in=filtered_journals))
    )

    # sort by ascent count by default
    mountainlist = mountainlist.order_by('-ascent_count')

    # order by height and name if selected
    if order_by == "height":
        mountainlist = mountainlist.order_by('-height_meters')
    if order_by == "name":
        mountainlist = mountainlist.order_by('name')

    # if there are no querys from sortting and filtering - revert back to orginal landing page 
    if len(mountainlist) == 0:
        # redirect to the same view with default query string
        return redirect(f'{request.path}')

    context['filter_by'] = filter_by
    context['order_by'] = order_by
    context['time_period'] = time_period
    context['grid_map'] = grid_map

    # store categories to make filter buttons
    context['cat_list'] = list(cat_list.values())
    context['cat_list'].sort()

    # check to see if there is a query
    query = request.GET.get('q')
    form = MountainSearchForm()

    if query:
        mountainlist = mountain.objects.filter(name__icontains=query)
        context['query'] = query
    
    if grid_map == 'map_view':
        mountains_json = json.dumps([{'name': mountain.name, 'lat': mountain.latitude, 'lon': mountain.longitude, 'country': mountain.country, 'height': mountain.height_meters, 'classification': mountain.classification, 'region': mountain.region} for mountain in mountainlist])
        context['mountains_json'] = mountains_json    

    # include pagination for handling of results per page
    paginator = Paginator(mountainlist, 6) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    mountainlist = paginator.get_page(page_number)

    context['mountainlist'] = mountainlist

    # get user details for navbar - pass user obj to profile model
    # user_profile_obj = user_profile(request)
    if request.user.username:
        user_object = User.objects.get(username=request.user.username)
        user_profile_obj = userProfile.objects.get(user=user_object)

    if request.user.is_authenticated:
        context['user_profile'] = user_profile_obj
        context['user_email'] = request.user.email
        context['first_name'] = user_object.first_name
        context['last_name'] = user_object.last_name
    else:
        context['user_profile'] = None

    # get user journal entries to get user activity
    user_activity = JournalEntry.objects.filter(mountain_fk__in=mountainlist)
    user_activity = user_activity.order_by('-date_climbed')

    # add user activity to the context
    context['user_activity'] = user_activity

    # get user stripe details, if subscribed
    if request.user.username:
        user_obj = User.objects.get(username=request.user.username)
        if StripeUser.objects.filter(user=user_obj).exists():
            stripe_user = StripeUser.objects.get(user=user_obj)
            if stripe_user.active_subscription():
                stripe_user_auth = True
            else: 
                stripe_user_auth = False
        else:
            stripe_user_auth = False

        # add stripe user condition to context
        context['stripe_user_auth'] = stripe_user_auth

    context['form'] = form

    return render(request, "landing_page.html", context)


cat_ls = [
    'Arderin',
    'Birkett',
    'Corbett',
    'Dodd',
    # 'Donald',
    'Furth',
    'Graham',
    'Hewitt',
    'Hump',
    'Marilyn',
    'Munro',
    'Nuttall',
    'Simm',
    # 'Tump',
    'Vandeleur-Lynam',
    'Wainwright'
]

country_progress_ls = [
    's', #scotland
    'e', #england
    'w', #wales
    'i' #ireland
]

country_progress_ls_full = [
    '🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland',
    '🏴󠁧󠁢󠁥󠁮󠁧󠁿 England',
    '🏴󠁧󠁢󠁷󠁬󠁳󠁿 Wales',
    '🇮🇪 Ireland'
]

# user dashboard view
# @login_required(login_url='home')
def profile_dashboard(request, first_name, last_name, id_user, *args, **kwargs):

    # declare context dictionary
    context = {}

    if request.user.username:
        user = User.objects.get(username=request.user.username)
        context['public_user'] = False
    else:  
        context['first_name'] = first_name
        context['last_name'] = last_name
        user = User.objects.get(first_name=first_name.capitalize(), last_name=last_name.capitalize())    
        context['public_user'] = True     

    user_profile = userProfile.objects.get(user=user)

    if int(user_profile.id_user) != int(id_user):
        return HttpResponseNotFound("Page Not Found") 

    journal_entries = JournalEntry.objects.all()

    # filter for user
    # user = User.objects.get(username=request.user.username)
    journal_entries = journal_entries.filter(user=user)

    # order by created at first
    journal_entries = journal_entries.order_by('-created_at')

    context['journal_entries'] = journal_entries 

    total_cat_counts = {}

    # get total counts for each mountain type/category
    for category in cat_ls:
        cat_counts = mountain.objects.filter(classification__icontains=category)
        cat_counts = cat_counts.values("classification").annotate(Count("id"))
        total_cat_counts[category] = int(list(cat_counts.aggregate(Sum('id__count')).values())[0])

    # get unique names from journal entries
    unique_journals = list(journal_entries.order_by('mountain_name').values_list('mountain_name', flat=True).distinct())

    # get user's total ascents to compare to absolute totals
    journal_mountain_objs = mountain.objects.filter(name__in=unique_journals)

    user_cat_counts = {}

    # get user ascend counts for each mountain type/category
    for category in cat_ls:
        journal_cat_counts = journal_mountain_objs.filter(classification__icontains=category)
        journal_cat_counts = journal_cat_counts.values("classification").annotate(Count("id"))
        user_cat_counts[category] = list(journal_cat_counts.aggregate(Sum('id__count')).values())[0]

    # replace 'none' values in dicionary with '0'
    user_cat_counts = { k: (0 if v is None else v) for k, v in user_cat_counts.items() }

    # create user progress dictionary
    user_progress_cat = ((np.array(list(user_cat_counts.values())) / np.array(list(total_cat_counts.values()))) * 100)

    # create dictionary for sorting of user % progress
    user_progress_cat_dict = dict(zip(user_cat_counts.keys() , user_progress_cat))

    # sort user percentage progress
    user_progress_cat_dict = dict(sorted(user_progress_cat_dict.items(), key=lambda item: item[1], reverse=True))

    # sort dictionary of user asecents relative to % progress
    user_cat_counts = dict(OrderedDict([(el, user_cat_counts[el]) for el in user_progress_cat_dict.keys()]))
    
    # sort total counts to match user % ascents
    total_cat_counts = dict(OrderedDict([(el, total_cat_counts[el]) for el in user_progress_cat_dict.keys()]))


    # pass to total and user category counts to conext
    context['total_category_counts'] = total_cat_counts
    context['user_category_counts'] = list(user_cat_counts.values()) 
    context['user_progress_cat'] = list(user_progress_cat_dict.values())

    # for example profile screenshot
    # context['total_category_counts'] = total_cat_counts
    # context['user_category_counts'] = np.array(list(user_cat_counts.values())) * 3
    # context['user_progress_cat'] = np.array(list(user_progress_cat_dict.values())) * 3

    # annotate each mountain with the ascent count for that mountain
    mountain_ascends_count = mountain.objects.annotate(
        ascent_count=Count('journal_entries')
    )

    context['mountain_ascends_count'] = mountain_ascends_count

    # get progress details relevant to country
    total_country_counts = {}

    # get total counts for each mountain type/category
    for idx, country in enumerate(country_progress_ls):
        country_counts = mountain.objects.filter(country__icontains=country)
        country_counts = country_counts.values("country").annotate(Count("id"))
        total_country_counts[country_progress_ls_full[idx]] = list(country_counts.aggregate(Sum('id__count')).values())[0]

    user_country_counts = {}

    # get user ascend counts for each mountain type/category
    for idx, country in enumerate(country_progress_ls):
        journal_country_counts = journal_mountain_objs.filter(country__icontains=country)
        journal_country_counts = journal_country_counts.values("country").annotate(Count("id"))
        user_country_counts[country_progress_ls_full[idx]] = list(journal_country_counts.aggregate(Sum('id__count')).values())[0]

    # replace 'none' values in dicionary with '0'
    user_country_counts = { k: (0 if v is None else v) for k, v in user_country_counts.items() }

    # sort by most climbed by user
    user_country_counts = dict(sorted(user_country_counts.items(), key=lambda item: item[1], reverse=True))

    # sort total counts to match user ascents
    total_country_counts = dict(OrderedDict([(el, total_country_counts[el]) for el in user_country_counts.keys()]))

    # create user progress dictionary breakdown for country
    user_progress_country = (np.array(list(user_country_counts.values())) / np.array(list(total_country_counts.values()))) * 100


    # pass to total and user country counts to conext
    context['total_country_counts'] = total_country_counts
    context['user_country_counts'] = list(user_country_counts.values())
    context['user_progress_country'] = list(user_progress_country)


    # get the current user profile additional details
    if request.user.username:
        user_object = User.objects.get(username=request.user.username)
    else:
        user_object = User.objects.get(first_name=first_name.capitalize(), last_name=last_name.capitalize()) 

    user_profile = userProfile.objects.get(user=user_object)

    context['user_profile'] = user_profile
    context['id_user'] = user_profile.id_user

    # edit profile functionailty
    if request.method == 'POST':
        
        if request.FILES.get('image-edit') == None:
            image = user_profile.profileimg
        elif request.FILES.get('image-edit') != None:
            image = request.FILES.get('image-edit')

        # bio = request.POST['bio']
        first_name_edit = request.POST['firstname_edit']
        second_name_edit = request.POST['surname_edit']
        city_edit = request.POST['city_edit']
        location_edit = request.POST['location_edit']

        user_profile.profileimg = image
        # user_profile.bio = bio
        user_object.first_name = first_name_edit
        user_object.second_name = second_name_edit
        user_profile.town_city = city_edit
        user_profile.location = location_edit

        user_profile.save()
        user_object.save()


        user_obj = User.objects.get(username=request.user.username)
        user_profile_obj = userProfile.objects.get(user=user_obj)

        first_name = user_obj.first_name
        last_name = user_obj.last_name
        id_user = user_profile_obj.id_user

        url = reverse('profile_dashboard', kwargs={'first_name': first_name.lower(), 'last_name': last_name.lower(), 'id_user': id_user})

        return redirect(url)
    
    # get corresponding mountain dirs from journal entries to allow for coordinates retrevial in template
    context['journal_mountain_objs'] = journal_mountain_objs  

    context['post_images'] = PostImage.objects.all()

    # get data for community update posts
    community_updates = JournalEntry.objects.all()
    # community_updates = JournalEntry.objects.all().exclude(user=request.user.username)

    # ensure sorted by date created in ascending order
    community_updates = community_updates.order_by('-created_at')

    # add to context
    context['community_updates'] = community_updates

    # add category list for leaderboard
    context['category_list'] = cat_ls

    # set leader board defaults
    leader_filter_category = 'Munro'
    leader_time_filter = 'leader-year'

    # add leaderboard conditioning and filtering
    if 'leader_filter_category' in request.GET:
        leader_filter_category = request.GET['leader_filter_category']
        leader_time_filter = request.GET['leader_time_filter']

    # filter the journal entries by time
    todays_date = datetime.today()
    if leader_time_filter == "leader-week":
        first_day_of_week = todays_date - timedelta(days=todays_date.weekday())
        leader_entries = JournalEntry.objects.filter(date_climbed__range=[first_day_of_week.strftime('%Y-%m-%d'), todays_date.strftime('%Y-%m-%d')])
    elif leader_time_filter == "leader-month":
        leader_entries = JournalEntry.objects.filter(date_climbed__range=[f"{todays_date.year}-{todays_date.month}-01", todays_date.strftime('%Y-%m-%d')])
    elif leader_time_filter == "leader-year":
        leader_entries = JournalEntry.objects.filter(date_climbed__range=[f"{todays_date.year}-01-01", todays_date.strftime('%Y-%m-%d')])
    elif leader_time_filter == "leader-all-time":
        leader_entries = JournalEntry.objects.all()  

    # get only the unique values 
    # leader_entries = leader_entries.values('mountain_fk__name').distinct()

    # get corresponding mountain objects from journal entries
    leader_entries = leader_entries.filter(mountain_fk__classification__contains=leader_filter_category)

    # make sure to only count unique values
    leader_entries = leader_entries.values('user__username').annotate(num_entries=Count('mountain_name', distinct=True))

    # Sort the entries by the number of entries in descending order
    leader_entries = leader_entries.order_by('-num_entries')

    # get the top 10 entrants
    leader_entries = leader_entries[:10]

    # add leader entries to context
    context['leader_entries'] = leader_entries

    # get the corresponding user profiles for the leaderboard
    leader_profiles = []
    for lead in leader_entries: 
        leader_profiles.append(User.objects.get(username=lead['user__username']))

    # add to context
    context['leader_profiles'] = leader_profiles 
    context['leader_filter_category'] = leader_filter_category
    context['leader_time_filter'] = leader_time_filter

    # get user stripe details, if subscribed
    # user_obj = User.objects.get(username=request.user.username)
    if request.user.username:
        if StripeUser.objects.filter(user=user_object).exists():
            stripe_user = StripeUser.objects.get(user=user_object)
            if stripe_user.active_subscription():
                stripe_user_auth = True
            else: 
                stripe_user_auth = False
        else:
            stripe_user_auth = False
    else:
        stripe_user_auth = False

    # add stripe user condition to context
    context['stripe_user_auth'] = stripe_user_auth

    # set default for journal entry limit to false
    journal_entry_lim = False

    # if stripe user auth is false check to see if journal entry limit is breached
    free_journal_lim = 5
    if stripe_user_auth == False:
        if journal_entries.count() >= free_journal_lim:
            journal_entry_lim = True

    # add journal entruy to context
    context['journal_entry_lim'] = journal_entry_lim

    if request.user.username:
        context['first_name'] = user.first_name
        context['last_name'] = user.last_name
    else:
        context['first_name'] = first_name
        context['last_name'] = last_name


    return render(request, "profile_dashboard.html", context)


@csrf_exempt
def register_request(request):

    if request.method == 'POST':

        if request.POST['firstname'] == "" or request.POST['surname'] == "" or request.POST['email'] == "" :
                messages.info(request, 'Please enter requested details to create an account')
                return redirect('home')

        firstname = request.POST['firstname']
        surname = request.POST['surname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        country = request.POST['signup-country']
        city = request.POST['signup-city']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'It looks like this email address is already registered')
                return redirect('home')
            else:
                username = email
                user = User.objects.create_user(username=username, first_name=firstname, last_name=surname, email=email, password=password)
                user.save()

                # log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                # create a Profile object for the new user
                user_model = User.objects.get(email=email)
                new_profile = userProfile.objects.create(user=user_model, id_user=user_model.id, location=country, town_city=city)
                new_profile.save()

                first_name = user_model.first_name
                last_name = user_model.last_name
                id_user = user_model.id
                
                url = reverse('profile_dashboard', kwargs={'first_name': first_name.lower(), 'last_name': last_name.lower(), 'id_user': id_user})

                return redirect(url)
        else:
            messages.info(request, 'Password not matching')
            return redirect('home')
        
    else:
        return render(request, 'landing_page.html')
    

def login_request(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=email, password=password)

        if user is not None:
            auth.login(request, user)

            user = User.objects.get(username=request.user.username)
            user_profile_obj = userProfile.objects.get(user=user)

            first_name = user.first_name
            last_name = user.last_name

            id_user = user_profile_obj.id_user
            
            url = reverse('profile_dashboard', kwargs={'first_name': first_name.lower(), 'last_name': last_name.lower(), 'id_user': id_user})

            return redirect(url)
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    else:
        return render(request, 'landing_page.html', {})



@login_required(login_url='home')
def edit_profile(request):

    user_profile = userProfile.objects.get(user=request.user)

    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
        elif request.FILES.get('image') != None:
            image = request.FILES.get('image')

        bio = request.POST['bio']
        location = request.POST['location']

        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()
        
        return redirect('edit_profile')
    
    return render(request, 'edit_profile.html', {'user_profile': user_profile})

# @login_required(login_url='login')
def logout_request(request):
    auth.logout(request)
    return redirect('home')


# @login_required(login_url='login')
def add_hike(request):

    # get user obj
    user_obj = User.objects.get(username=request.user.username)
    user_profile_obj = userProfile.objects.get(user=user_obj)

    first_name = user_obj.first_name
    last_name = user_obj.last_name
    id_user = user_profile_obj.id_user

    url = reverse('profile_dashboard', kwargs={'first_name': first_name.lower(), 'last_name': last_name.lower(), 'id_user': id_user})

    if request.method == 'POST':

        # check to make sure user has entered a relavant mountain name and climb date
        if not mountain.objects.filter(name=request.POST['mountain-name']).exists() or not request.POST['date-climbed']:
            messages.info(request, 'Please select a mountain name from the dropdown list and enter a climb date in the correct format')
            return redirect(url)

        # user = request.user.username
        # image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        mountain_name = request.POST['mountain-name']
        date_climbed = request.POST['date-climbed']

        # get the corrsponding mountain obj for the current entry
        current_mountain_obj = mountain.objects.get(name=mountain_name)

        new_post = JournalEntry.objects.create(user=user_obj, caption=caption, mountain_name=mountain_name, date_climbed=date_climbed, mountain_fk=current_mountain_obj)
        new_post.save()

        # save images 
        if request.FILES.get('journal-images') != None:
            for img in request.FILES.getlist('journal-images'):
                postimage = PostImage()
                postimage.post = new_post
                postimage.image = img
                postimage.save()

        # each time hike added increment total ascent counter (total)
        current_hike = mountain.objects.get(name=mountain_name)
        current_hike.ascend_count += 1
        current_hike.save()

    return redirect(url)


def remove_post(request):
    # get current post id
    post_id = request.POST.get('delete-post-btn') 
    post = JournalEntry.objects.get(id=post_id)
    post.delete()

    user_obj = User.objects.get(username=request.user.username)
    user_profile_obj = userProfile.objects.get(user=user_obj)

    first_name = user_obj.first_name
    last_name = user_obj.last_name
    id_user = user_profile_obj.id_user

    url = reverse('profile_dashboard', kwargs={'first_name': first_name.lower(), 'last_name': last_name.lower(), 'id_user': id_user})
    
    return redirect(url)



# create mountain search function:
def search_mountain_names(request):
    mountain_name = request.GET.get('mountain_name')
    payload = []
    if mountain_name:
        mountains_objs = mountain.objects.filter(name__icontains=mountain_name)

        for mountain_obj in mountains_objs:
            payload.append(mountain_obj.name)

    return JsonResponse({'status': 200, 'data': payload})



endpoint_secret = env('STRIPE_ENDPOINT_SECRET') # live




# This is your Stripe CLI webhook secret for testing your endpoint locally.

@csrf_exempt
def stripe_webhook(request):
    event = None
    payload = request.body
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'checkout.session.completed':

        session = event['data']['object']
        user_email = session['customer_details']['email']

        # session_id = session.get('id', None)
        # line_items = stripe.checkout.Session.list_line_items(session_id)
        # line_items = json.loads(str(line_items['data'][0]))

        # get user credentials from payment session
        # customer = stripe.Customer.retrieve(session.customer)
        # current_user = get_object_or_404(User, email=user_email)

        # update stripe user model
        current_user = User.objects.get(email=user_email)

        # (15, null, null, f, 0, False, False, False, False, 2023-11-29 18:17:59+00, null, 1)
        now = datetime.now()

        stripe_user = StripeUser.objects.create(
                                                # stripe_subscription_id=False, 
                                                # is_paid=False, 
                                                # price=False, 
                                                # stripe_price_id=False, 
                                                # plan=False, 
                                                # stripe_product=False, 
                                                # recurring_interval=False,
                                                # created_at=str(now.strftime('%Y-%m-%d %H:%M:%S.%f%z')),
                                                # end_date_of_subscription=False,
                                                user=current_user)

        # update in django model
        stripe_user.customer_id = session.get('customer', stripe_user.customer_id)
        stripe_user.stripe_subscription_id = session.get('subscription', stripe_user.stripe_subscription_id) or ''
        print(session.get('subscription', stripe_user.stripe_subscription_id))
        stripe_user.is_paid = True  # Assuming this is always set
        stripe_user.price = session.get('amount_total', stripe_user.price) or ''
        stripe_user.stripe_price_id = session.get('payment_method_configuration_details', {}).get('id', stripe_user.stripe_price_id) or ''
        stripe_user.plan = 'Pro'
        stripe_user.stripe_product = session.get('subscription', stripe_user.stripe_product) or ''
        stripe_user.recurring_interval = 'Monthly'  # Assuming this is always set
        stripe_user.active_subscription = True  # Assuming this is always set
        stripe_user.save()

    # ... handle other event types
    # elif event['type'] == 'checkout.session.completed' and :

    else:
      HttpResponse(status=200)

    return HttpResponse(status=200)







def create_customer_portal_session(request):
    stripe.api_key = env('STRIPE_API_KEY') # live


    # Authenticate your user.
    user = User.objects.get(username=request.user.username)

    user_profile_obj = userProfile.objects.get(user=user)

    first_name = user.first_name
    last_name = user.last_name
    user_id = user_profile_obj.id_user

    stripe_user_portal = StripeUser.objects.get(user=user)
    session = stripe.billing_portal.Session.create(
        customer=  stripe_user_portal.customer_id,
        return_url=f'https://www.donder.co.uk/{first_name}-{last_name}-{user_id}',
    )
    return redirect(session.url)

def success_request(request):
    messages.info(request, "You have successfully subscribed.") 
    return redirect("home")

def cancel_request(request):
    messages.info(request, "Payment Failed. Please try again.") 
    return redirect("home")

def get_time_since_last_update(request):
    post_id = request.GET.get('post_id')
    post = JournalEntry.objects.get(id=post_id)
    time_diff = timezone.now() - post.created_at

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


    return JsonResponse({'time_diff': time_since})



def get_community_modal(request):

    # get current post id 
    post_id = request.POST.get('post_id')

    # get corresponding journal entry obj
    journal_obj = JournalEntry.objects.get(id=post_id)

    # get all mountaindirs objs
    mountain_objs = mountain.objects.all()

    # get post images for current jounral entry
    image_objs = PostImage.objects.all()

    # annotate each mountain with the ascent count for that mountain
    mountain_ascends_count = mountain.objects.annotate(
        ascent_count=Count('journal_entries')
    )
    
    # pass context params necessary for modal render
    context =  {
        'jounral_entry': journal_obj,
        'journal_mountain_objs': mountain_objs,
        'post_images': image_objs,
        'mountain_ascends_count': mountain_ascends_count
    }

    html = render_to_string('community_modal_content.html', context=context)

    response = HttpResponse(html)

    return response



def leaderboard(request):

    context = {}

    leader_filter_category = request.GET['leader_filter_category']
    leader_time_filter = request.GET['leader_time_filter']

    context['leader_filter_category'] = leader_filter_category
    context['leader_time_filter'] = leader_time_filter

    return redirect(request, "profile_dashboard.html", context=context)
    

# most-popular 
def most_popular_climbs(request, mountain_type, country):

    # set default data
    mountainlist = mountain.objects.all()
    filter_by = request.GET.get('filter_by', country)
    order_by = request.GET.get('order_by', 'ascents')
    class_type = request.GET.get('class_type', mountain_type)
    time_period = request.GET.get('time_period', 'all_time')
    grid_map = request.GET.get('grid_map', 'grid_view')
    context = {}

    if request.method == "POST":
        email = request.POST['login-email']
        password = request.POST['login-password']

        user = auth.authenticate(username=email, password=password)

        if user is not None:
            auth.login(request, user)

            user_obj = User.objects.get(username=request.user.username)
            user_profile_obj = userProfile.objects.get(user=user_obj)

            first_name = user_obj.first_name
            last_name = user_obj.last_name
            id_user = user_profile_obj.id_user

            url = reverse('profile_dashboard', kwargs={'first_name': first_name.lower(), 'last_name': last_name.lower(), 'id_user': id_user})

            return redirect(url)
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('home') # additional logic implemented into login modal to prompt reload if error

    if filter_by == 'all':
        mountainlist = mountain.objects.all()
    elif filter_by == 'scotland':
        mountainlist = mountain.objects.filter(country='S')
    elif filter_by == 'ireland':
        mountainlist = mountain.objects.filter(country='I')
    elif filter_by == 'england':
        mountainlist = mountain.objects.filter(country='E')
    elif filter_by == 'wales':
        mountainlist = mountain.objects.filter(country='W')

    if class_type:
        mountainlist = mountainlist.filter(classification__icontains=class_type)

    # filtered journal entry objects
    filtered_names = mountainlist.values_list('name', flat=True)
    filter_journals = JournalEntry.objects.filter(mountain_fk__name__in=filtered_names)

    # now filter journal entries to get ascent counts
    todays_date = datetime.today()
    if time_period == "last_24hrs":
        yesterday = todays_date - timedelta(days=1)
        filtered_journals = filter_journals.filter(date_climbed__range=[yesterday.strftime('%Y-%m-%d'), todays_date.strftime('%Y-%m-%d')])
    if time_period == "this_week":
        first_day_of_week = todays_date - timedelta(days=todays_date.weekday())
        filtered_journals = filter_journals.filter(date_climbed__range=[first_day_of_week.strftime('%Y-%m-%d'), todays_date.strftime('%Y-%m-%d')])
    elif time_period == "this_month":
        filtered_journals = filter_journals.filter(date_climbed__range=[f"{todays_date.year}-{todays_date.month}-01", todays_date.strftime('%Y-%m-%d')])
    elif time_period == "this_year":
        filtered_journals = filter_journals.filter(date_climbed__range=[f"{todays_date.year}-01-01", todays_date.strftime('%Y-%m-%d')])
    elif time_period == "all_time":
        filtered_journals = filter_journals 
    

    # annotate each mountain with the ascent count for that mountain
    mountainlist = mountainlist.annotate(
        ascent_count=Count('journal_entries', filter=Q(journal_entries__in=filtered_journals))
    )

    # sort by ascent count by default
    mountainlist = mountainlist.order_by('-ascent_count')

    # order by height and name if selected
    if order_by == "height":
        mountainlist = mountainlist.order_by('-height_meters')
    if order_by == "name":
        mountainlist = mountainlist.order_by('name')

    # if there are no querys from sortting and filtering - revert back to orginal landing page 
    if len(mountainlist) == 0:
        # redirect to the same view with default query string
        return redirect(f'{request.path}')

    context['filter_by'] = filter_by
    context['order_by'] = order_by
    context['time_period'] = time_period
    context['class_type'] = class_type
    context['grid_map'] = grid_map
    

    # store categories to make filter buttons
    context['cat_list'] = list(cat_list.values())
    context['cat_list'].sort()

    # include pagination for handling of results per page
    paginator = Paginator(mountainlist, 6) # Show 6 contacts per page.
    page_number = request.GET.get('page')
    mountainlist = paginator.get_page(page_number)


    context['mountainlist'] = mountainlist

    # get user details for navbar - pass user obj to profile model
    # user_profile_obj = user_profile(request)
    if request.user.username:
        user_object = User.objects.get(username=request.user.username)
        user_profile_obj = userProfile.objects.get(user=user_object)

    if request.user.is_authenticated:
        context['user_profile'] = user_profile_obj
        context['user_email'] = request.user.email
    else:
        context['user_profile'] = None

    # get user journal entries to get user activity
    user_activity = JournalEntry.objects.filter(mountain_fk__in=mountainlist)
    user_activity = user_activity.order_by('-date_climbed')

    # add user activity to the context
    context['user_activity'] = user_activity

    # get user stripe details, if subscribed
    if request.user.username:
        user_obj = User.objects.get(username=request.user.username)
        if StripeUser.objects.filter(user=user_obj).exists():
            stripe_user = StripeUser.objects.get(user=user_obj)
            if stripe_user.active_subscription():
                stripe_user_auth = True
            else: 
                stripe_user_auth = False
        else:
            stripe_user_auth = False

        # add stripe user condition to context
        context['stripe_user_auth'] = stripe_user_auth

    return render(request, "most_popular.html", context)



def search_icon(request):
    return render(request, "search-icon.html")


