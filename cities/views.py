from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView

from cities.models import City


def home(request, pk=None):
    if pk:
        # city = City.objects.filter(id=pk).first()
        city = get_object_or_404(City, id=pk)
        return render(request, 'cities/detail.html', {'object': city, })
    cities = City.objects.all()
    context = {'objects_list': cities, }
    return render(request, 'cities/home.html', context)


class CityDetailView(DetailView):
    queryset = City.objects.all()
    context_object_name = 'object'
    template_name = 'cities/detail.html'
