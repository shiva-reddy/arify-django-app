import os
import sys

from django.core.files import File
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.shortcuts import render

# Create your views here.
from django.template import loader

from arify_app.FileUploadDownloadUtil import upload_to_aws
from arify_app.forms import SceneNameForm, ARObjectForm, UploadForm
from arify_app.models import Scene, Ar_object, Image_target_ar_object, Image_target
from arify_backend import urls, settings


def index(request):
    scenes_list = Scene.objects.all()
    template = loader.get_template('arify_app/index.html')
    context = {
        'scenes_list': list(map(lambda s : s.name, scenes_list)),
        'upload_form': UploadForm()
    }
    return HttpResponse(template.render(context, request))

def add_scene(request):
    if request.method == "POST":
        scene_name = request.POST.get('scene_name')
        used_scene_names = list(map(lambda s : s.name, Scene.objects.all()))
        if scene_name not in used_scene_names:
            Scene.add_scene(scene_name)
    return HttpResponseRedirect("/")

def download_file(uploaded_file):
    fd = open("uploads/" + str(uploaded_file.name), 'wb')
    for chunk in uploaded_file.chunks():
        fd.write(chunk)
    fd.close()
    print("Saved file at " + fd.name)
    return fd.name


def add_ar_object(request):
    if request.method == "POST":
        file_name = request.FILES['file'].name
        downloaded_file_path = download_file(request.FILES['file'])
        print("Downloaded file to " + downloaded_file_path)
        aws_path = settings.ENV + "/ar_objects/" + file_name
        print("Uploading to AWS s3 at " + aws_path)
        upload_to_aws(downloaded_file_path, settings.BUCKET_NAME, aws_path)

        # chosen_scene = request.POST.get('chosen_scene')
        # object_name = request.POST.get('object_name')
        # used_object_names = list(map(lambda s: s.name, Ar_object.objects.filter(scene__name = chosen_scene)))
        # if object_name not in used_object_names:
        #     object_file = request.POST.get('file')
        #     print(type(object_file))
        #     print(object_file)
        #     file_link = upload_file("ar_objects", object_file)
        #     Ar_object.add_object(chosen_scene, object_name, file_link)
        #     print("here")
    return HttpResponseRedirect("/")


def upload_file(folder, file):
    env = "dev/"
    path = env + folder
    # link = upload_to_aws(file, path, file)
    link ="https://www.google.com"
    return link

def list_ar_objects(request, pk):
    data = {"results": list(map(lambda ar_object: {"name": ar_object.name, "link": ar_object.link}, Ar_object.objects.filter(scene__name=pk)))}
    return JsonResponse(data)

def list_image_targets(request, pk):
    data = {"results": list(map(lambda image_target: {"name": image_target.name, "link": image_target.link}, Image_target.objects.filter(scene__name=pk)))}
    return JsonResponse(data)

def upload_image(request, pk):
    image = get_file_from_request(request)
    _name = request.POST.get('image_name')
    _scene = Scene.objects.filter(name=pk)

    if len(_scene) == 0:
        return error_json("Scene is not present")

    used_image_target_names = list(map(lambda s: s.name, Image_target.objects.filter(scene__name = pk)))
    if _name in used_image_target_names:
        return error_json("Name is already used for current scene")

    _link = upload_file("image_targets",image)
    # _link = "https://www.google.com"

    image_target = Image_target(name = _name, scene=_scene[0],link=_link)
    image_target.save()
    return success()

def link_image_with_ar_object(request, pk):
    _image_name = request.POST.get('image_name')
    _object_name = request.POST.get('ar_object_name')
    _scene = Scene.objects.filter(name=pk)
    if len(_scene) == 0:
        return error_json("Scene is not present")
    _image_target = Image_target.objects.filter(name=_image_name)
    _ar_object = Ar_object.objects.filter(name=_object_name)
    image_target_ar_object = Image_target_ar_object(scene = _scene, image_target = _image_target, ar_object=_ar_object)
    image_target_ar_object.save()
    return success()

def success():
    data = {}
    return JsonResponse(data)

def error_json(message):
    data = {"error":message}
    return JsonResponse(data)

def get_file_from_request(request):
    return request

def scenes_list(request):
    scenes = Scene.objects.all()
    data = {"results": list(scenes.values("name"))}
    return JsonResponse(data)

def scene_links(request, pk):
    links = Image_target_ar_object.objects.filter(scene__name = pk)
    data = {"results": list(map(lambda link: link_json(link), links))}
    return JsonResponse(data)

def link_json(link):
    image_target_link = link.image_target.link
    ar_object_link = link.ar_object.link
    image_target = {"name": link.image_target.name, "link":image_target_link}
    ar_object = {"name": link.ar_object.name, "link": ar_object_link}
    return {"image_target": image_target, "ar_object": ar_object}