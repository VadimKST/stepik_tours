import random

from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404

from tours.data import title, subtitle, description, tours, departures


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')


def custom_handler404(request, exception):
    return HttpResponseNotFound('Страница не найдена!')


def main_view(request):
    tours_rand = random.sample(tours.items(), 6)
    return render(request, 'tours/index.html', {
        'title': title,
        'subtitle': subtitle,
        'description': description,
        'tours_rand': tours_rand
    })


msk_deps = [(i, tours[i]) for i in tours if tours[i]['departure'] == 'msk']
spb_deps = [(i, tours[i]) for i in tours if tours[i]['departure'] == 'spb']
nsk_deps = [(i, tours[i]) for i in tours if tours[i]['departure'] == 'nsk']
ekb_deps = [(i, tours[i]) for i in tours if tours[i]['departure'] == 'ekb']
kazan_deps = [(i, tours[i]) for i in tours if tours[i]['departure'] == 'kazan']

city_deps = {
    'msk': msk_deps,
    'spb': spb_deps,
    'nsk': nsk_deps,
    'ekb': ekb_deps,
    'kazan': kazan_deps
}


def departure_view(request, departure):
    try:
        city_deps[departure]
    except KeyError:
        raise Http404()
    coasts = sorted(city_deps[departure], key=lambda x: x[1]['price'])
    min_coast = coasts[0][1]["price"]
    max_coast = coasts[-1][1]["price"]
    nights = sorted(city_deps[departure], key=lambda x: x[1]['nights'])
    min_night = nights[0][1]["nights"]
    max_night = nights[-1][1]["nights"]
    return render(request, 'tours/departure.html', {
        'city_deps': city_deps[departure],
        'len_dep': len(city_deps[departure]),
        'min_coast': min_coast,
        'max_coast': max_coast,
        'min_night': min_night,
        'max_night': max_night,
        'city': departures[departure]
    })


def tour_view(request, id):
    try:
        tours[id]
    except KeyError:
        raise Http404()
    return render(request, 'tours/tour.html', {
        'tour': tours[id],
        'tour_departure': departures[tours[id]['departure']]
    })
