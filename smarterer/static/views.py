from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest

def index(request):

    data = {
        'page_count': range(9)
    }

    return render(request, 'static/index.html', data)
