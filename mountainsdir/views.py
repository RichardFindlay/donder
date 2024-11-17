from django.shortcuts import render
from .models import mountain
from .forms import MountainSearchForm


def search_mountains(request):
    query = request.GET.get('q')
    form = MountainSearchForm()
    if query:
        mountains = mountain.objects.filter(name__icontains=query)
    else:
        mountains = None
    return render(request, 'landing_page.html', {'mountains': mountains, 'query': query, 'form': form})