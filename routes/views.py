from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import DetailView, ListView

from trains.models import Train
from .forms import *
from .models import Route
from .utils import get_routes


def home(request):
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})


def find_routes(request):
    if request.method == "POST":
        form = RouteForm(request.POST or None)
        if form.is_valid():
            try:
                context = get_routes(request, form)
            except ValueError as e:
                messages.error(request, e)
                return render(request, 'routes/home.html', {'form': form})
            return render(request, 'routes/home.html', context)
    else:
        messages.error(request, 'Создайте маршрут')
        form = RouteForm()
        return render(request, 'routes/home.html', {'form': form})


def add_route(request):
    if request.method == 'POST':
        data = request.POST
        context = {}
        if data:
            context = {}
            travel_times = data['travel_times']
            from_city = data['from_city']
            to_city = data['to_city']
            trains = data['trains'].split(' ')
            trains_lst = [int(x) for x in trains if x.isalnum()]
            qs = Train.objects.filter(id__in=trains_lst)
            train_list = ' '.join(str(i) for i in trains_lst)
            # передача начальных данных в форму
            form = RouteModelForm(
                initial={'from_city': from_city, 'to_city': to_city,
                         'travel_times': travel_times, 'trains': train_list})
            route_desc = []
            for tr in qs:
                dsc = '''Поезд №{} следующий из г.{} в г.{}
            . Время в пути {}.'''.format(tr.name, tr.from_city, tr.to_city,
                                         tr.travel_time)
                route_desc.append(dsc)
            context = {'form': form, 'descr': route_desc,
                       'from_city': from_city,
                       'to_city': to_city, 'travel_times': travel_times}

        return render(request, 'routes/create.html', context)
    else:
        # защита от обращения по адресу без данных
        messages.error(request, 'Невозможно сохранить несуществующий маршрут')
        return redirect('/')


def save_route(request):
    if request.method == 'POST':
        data = request.POST
        context = {}
        if data:
            context = {}
            travel_times = data['travel_times']
            name = data['name']
            from_city = data['from_city']
            to_city = data['to_city']
            trains = data['trains'].split(' ')
            trains_lst = [int(x) for x in trains if x.isalnum()]
            qs = Train.objects.filter(id__in=trains_lst)
            route = Route(name=name, from_city=from_city,
                          to_city=to_city, travel_times=travel_times)
            route.save()  # сохранение нового маршрута
            # сохранение в маршруте, поездов из списка
            # for tr in trains_lst: # можно в цикле
            # route.trains.add(tr)
            route.trains.set(qs)  # если есть QuerySet, то можно так
            messages.success(request, 'Маршрут был успешно сохранен.')
            return redirect('/')

        return render(request, 'routes/create.html', context)
    else:
        # защита от обращения по адресу без данных
        messages.error(request, 'Невозможно сохранить несуществующий маршрут')
        return redirect('/')


class RouteDetailView(DetailView):
    queryset = Route.objects.all()
    template_name = 'routes/detail.html'


class RouteListView(ListView):
    queryset = Route.objects.all()
    # context_object_name = 'objects_list'
    template_name = 'routes/list.html'
    paginate_by = 2
