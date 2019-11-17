import sys

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.template import loader

from arify_app.forms import SceneNameForm, ARObjectForm
from arify_app.models import Scene, Ar_object
from arify_backend import urls


def index(request):
    print("here")
    scenes_list = Scene.objects.all()
    template = loader.get_template('arify_app/index.html')
    context = {
        'scenes_list': list(map(lambda s : s.name, scenes_list))
    }
    return HttpResponse(template.render(context, request))

def add_scene(request):
    if request.method == "POST":
        # scene_name_form = SceneNameForm(request.POST)
        # scene_name = scene_name_form.cleaned_data['scene_name']
        scene_name = request.POST.get('scene_name')
        used_scene_names = list(map(lambda s : s.name, Scene.objects.all()))
        if scene_name not in used_scene_names:
            Scene.add_scene(scene_name)
    return HttpResponseRedirect("/")

def add_ar_object(request):
    if request.method == "POST":
        # ar_object_form = ARObjectForm(request.POST)
        chosen_scene = request.POST.get('chosen_scene')
        object_name = request.POST.get('object_name')
        used_object_names = list(map(lambda s: s.name, Ar_object.objects.filter(scene__name = chosen_scene)))
        if object_name not in used_object_names:
            object_file = request.POST.get('file')
            file_link = upload_file(object_file)
            Ar_object.add_object(chosen_scene, object_name, file_link)
    return HttpResponseRedirect("/")

def upload_file(file):
    link ="https://www.google.com"
    return link