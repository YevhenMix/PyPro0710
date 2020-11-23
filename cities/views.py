from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from cities.forms import HtmlForm, CityForm
from cities.models import City


def home(request, pk=None):
    # if request.method == 'POST':
    #     form = CityForm(request.POST or None)
    #     print(request.POST)
    #     if form.is_valid():
    #         print(form.cleaned_data)
    #         form.save()
    cities = City.objects.all()
    paginator = Paginator(cities, 3)
    page = request.GET.get('page')
    cities = paginator.get_page(page)
    context = {'objects_list': cities, }
    return render(request, 'cities/home.html', context)



class CityDetailView(DetailView):
    queryset = City.objects.all()
    context_object_name = 'object'
    template_name = 'cities/detail.html'


class CityCreateView(SuccessMessageMixin, CreateView):
    model = City
    form_class = CityForm
    template_name = 'cities/create.html'
    success_url = reverse_lazy('cities:home')
    success_message = 'Город успешно создан!'


class CityUpdateView(UpdateView):
    model = City
    form_class = CityForm
    template_name = 'cities/update.html'
    success_url = reverse_lazy('cities:home')


class CityDeleteView(DeleteView):
    model = City
    # template_name = 'cities/delete.html'
    success_url = reverse_lazy('cities:home')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
