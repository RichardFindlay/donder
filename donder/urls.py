"""donder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .sitemaps import MostPopularSitemap, StaticSitemap, IndexSitemap #import StaticSitemap
from django.views.generic.base import TemplateView


from pages.views import landing_page, profile_dashboard, register_request, login_request, logout_request, edit_profile, add_hike, search_mountain_names, success_request, cancel_request, get_time_since_last_update, get_community_modal, leaderboard, stripe_webhook, create_customer_portal_session, remove_post, most_popular_climbs, search_icon
from mountainsdir.views import search_mountains


# config sitemaps
sitemaps = {
    'static': StaticSitemap,
    'mostpopular': MostPopularSitemap, 
    'indexes': IndexSitemap
}

urlpatterns = [
    path('', landing_page, name='home'),
    path('admin/', admin.site.urls),
    path("register", register_request, name="register"),
    path("login", login_request, name="login"),
    path("logout", logout_request, name="logout"),
    path("edit_profile", edit_profile, name="edit_profile"),
    path('<str:first_name>-<str:last_name>-<str:id_user>', profile_dashboard, name='profile_dashboard'),
    # re_path(r'^(?P<first_name>\w+)-(?P<last_name>\w+)-(?P<id_user>\d+)/$', profile_dashboard, name='profile_dashboard'),
    path("add_hike/", add_hike, name="add_hike"),
    path("remove_post", remove_post, name="remove_post"),
    path("search/", search_mountain_names, name="search_mountain_names"),
    path('success/', success_request, name="success"),
    path('cancel/', cancel_request, name="cancel"),
    path('get_time_since_last_update/', get_time_since_last_update, name='get_time_since_last_update'),
    path('get_community_modal/', get_community_modal, name='modal_content'),
    path('leaderboard', leaderboard, name='leaderboard'),
    path('stripe_webhook', stripe_webhook, name='stripe_webhook'),
    path('stripe_webhook/we_1MzpISCMR7u1SC0MZINrHA7L', stripe_webhook, name='stripe_webhook2'),
    path('create-customer-portal-session', create_customer_portal_session, name='create-customer-portal-session'),
    # custom url for most popular climbs
    path('most-popular-<mountain_type>s-in-<country>', most_popular_climbs),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('donder-search-icon', search_icon, name="search-icon"),
    path('', landing_page, name='search_mountains')

] + staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




print(urlpatterns)






    
