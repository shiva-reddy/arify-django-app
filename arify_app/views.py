from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader

from arify_app.models import Scene


def index(request):
    scenes_list = Scene.objects.all()
    template = loader.get_template('arify_app/index.html')
    context = {
        'scenes_list': list(map(lambda s : s.name, scenes_list))
    }
    return HttpResponse(template.render(context, request))