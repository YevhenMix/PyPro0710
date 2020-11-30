from trains.models import Train


def dfs_paths(graph, start, goal):
    """Функция поиска всех возможных маршрутов
    из одного города в другой. Вариант посещения
    одного и того же города более одного раза,
    не рассматривается.
    """
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_graph(_qs):
    qs = _qs.values()
    graph = {}
    for q in qs:
        graph.setdefault(q['from_city_id'], set())
        graph[q['from_city_id']].add(q['to_city_id'])
    return graph


def get_routes(request, form):
    '''
    Функция поиска маршрута
    :param request: request
    :param form: форма с начальными данными от пользователя
    :return: список маршрутов, готовых для отображения
    '''
    qs = Train.objects.all().order_by('travel_time')
    data = form.cleaned_data
    from_city = data['from_city']
    to_city = data['to_city']
    cities = data['cities']
    travelling_time = data['travelling_time']
    graph = get_graph(_qs=qs)
    all_ways = list(dfs_paths(graph, from_city.id, to_city.id))
    if len(all_ways) == 0:
        # нет ни одного маршрута для данного поиска
        raise ValueError('Маршрута, удовлетворяющего условиям не существует.')

    if cities:
        # если есть города, через которые нужно проехать
        across_cities = [city.id for city in cities]
        right_ways = []
        for way in all_ways:
            # тогда отбираем те маршруты, которые проходят через них
            if all(point in way for point in across_cities):
                right_ways.append(way)
        if not right_ways:
            # когда список маршрутов пуст
            raise ValueError('Маршрут, через эти города невозможен ')
    else:
        right_ways = all_ways
    trains = []
    all_trains = {}
    for q in qs:
        all_trains.setdefault((q.from_city_id, q.to_city_id), [])
        all_trains[(q.from_city_id, q.to_city_id)].append(q)

    for route in right_ways:
        # для городов по пути следования, выбираем необходимые поезда
        tmp = {}
        tmp['trains'] = []
        total_time = 0
        for index in range(len(route) - 1):
            qs = all_trains[(route[index], route[index + 1])]
            qs = qs[0]
            total_time += qs.travel_time
            tmp['trains'].append(qs)
            tmp['total_time'] = total_time
        if total_time <= travelling_time:
            # если общее время в пути, меньще заданного,
            # то добавляем маршрут в общий список
            trains.append(tmp)
    if not trains:
        # если список пуст, то нет таких маршрутов,
        # которые удовлетворяли бы заданным условиям
        raise ValueError('Время в пути, больше заданного.')
    routes = []
    cities = {'from_city': from_city.name, 'to_city': to_city.name}
    for tr in trains:
        # формирую список всех маршрутов
        routes.append({'trains': tr['trains'],
                       'total_time': tr['total_time'],
                       'from_city': from_city.name,
                       'to_city': to_city.name})
    sorted_routes = []
    if len(routes) == 1:
        sorted_routes = routes
    else:
        # если маршрутов больше одного, то сортирую их по времени
        times = list(set(x['total_time'] for x in routes))
        times = sorted(times)
        for time in times:
            for route in routes:
                if time == route['total_time']:
                    sorted_routes.append(route)
    context = {}
    context['form'] = form
    context['routes'] = sorted_routes
    context['cities'] = cities
    return context
