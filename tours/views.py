from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')


def custom_handler404(request, exception):
    return HttpResponseNotFound('Страница не найдена!')


def main_view(request):
    return render(request, 'tours/index.html')


def departure_view(request, departure):
    return render(request, 'tours/departure.html')


def tour_view(request, id):
    return render(request, 'tours/tour.html')
