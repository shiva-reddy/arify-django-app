import os
import sys

from django.core.files import File
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.shortcuts import render

# Create your views here.
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

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
        chosen_scene = request.POST.get('chosen_scene')
        object_name = request.POST.get('object_name')
        used_object_names = list(map(lambda s: s.name, Ar_object.objects.filter(scene__name = chosen_scene)))
        if object_name not in used_object_names:
            file_link = upload_file("/ar_objects/", request, 'file')
            obj_type = request.POST.get('object_type')
            mtl_file = None
            try:
                mtl_file = upload_file("/ar_objects/", request)
            except:
                mtl_file = None
            scale_x = getOrDefault(request.POST.get('scale_x'), 0.5)
            scale_y = getOrDefault(request.POST.get('scale_y'), 0.5)
            scale_z = getOrDefault(request.POST.get('scale_z'), 0.5)
            rot_x = getOrDefault(request.POST.get('rot_x'), 0.0)
            rot_y = 0.0
            rot_z = getOrDefault(request.POST.get('rot_z'), 0.0)
            pos_offset_x = getOrDefault(request.POST.get('pos_offset_x'), 0.0)
            pos_offset_y = getOrDefault(request.POST.get('pos_offset_y'), 0.0)
            pos_offset_z = getOrDefault(request.POST.get('pos_offset_z'), 0.0)

            Ar_object.add_object(chosen_scene, object_name, file_link,mtl_file,obj_type, scale_x, scale_y, scale_z, rot_x, rot_y, rot_z, pos_offset_x, pos_offset_y, pos_offset_z)
    return HttpResponseRedirect("/")

def getOrDefault(value, defValue):
    return defValue if (value == "") else value

def upload_file(folder, request, key):
    file_name = request.FILES[key].name
    downloaded_file_path = download_file(request.FILES[key])
    print("Downloaded file to " + downloaded_file_path)
    aws_path = os.environ['env'] + folder + file_name
    print("Uploading to AWS s3 at " + aws_path)
    return upload_to_aws(downloaded_file_path, settings.BUCKET_NAME, aws_path)


def list_ar_objects(request, pk):
    data = {"results": list(map(lambda ar_object: {"name": ar_object.name, "link": ar_object.link}, Ar_object.objects.filter(scene__name=pk)))}
    return JsonResponse(data)

def list_image_targets(request, pk):
    data = {"results": list(map(lambda image_target: {"name": image_target.name, "link": image_target.link}, Image_target.objects.filter(scene__name=pk)))}
    return JsonResponse(data)

def upload_image_ui(request):
    _name = request.POST.get('image_name')
    _scene = request.POST.get('chosen_scene')
    upload_image(request, _name, _scene)
    return HttpResponseRedirect("/")

def upload_image(request, _name, _scene_name):
    used_image_target_names = list(map(lambda s: s.name, Image_target.objects.filter(scene__name = _scene_name)))
    _scene = Scene.objects.filter(name=_scene_name)[0]
    if _name in used_image_target_names:
        return error_json("Name is already used for current scene")
    file_link = upload_file("/image_targets/", request, 'file')
    image_target = Image_target(name = _name, scene=_scene, link=file_link)
    image_target.save()

def update_ar_object_api(request, pk):
    _name = request.POST.get('ar_object_name')
    _scene = Scene.objects.filter(name=pk)
    if _scene.count() == 0:
        return error_json("Scene is not present")
    ar_object = Ar_object.objects.filter(name=_name, scene =_scene)
    scale_x = request.POST.get('scale_x', 0.5)
    scale_y = request.POST.get('scale_y', 0.5)
    scale_z = request.POST.get('scale_z', 0.5)
    rot_x = request.POST.get('rot_x', 0.0)
    rot_z = request.POST.get('rot_z', 0.0)
    pos_x = request.POST.get('pos_offset_x', 0.0)
    pos_y = request.POST.get('pos_offset_y', 0.0)
    pos_z = request.POST.get('pos_offset_z', 0.0)
    update_ar_object(ar_object, scale_x, scale_y, scale_z, rot_x, rot_z, pos_x, pos_y, pos_z)


def update_ar_object(ar_object, scale_x, scale_y, scale_z, rot_x, rot_z, pos_x, pos_y, pos_z):
    ar_object.rot_x = rot_x
    ar_object.rot_z = rot_z
    ar_object.scale_x = scale_x
    ar_object.scale_y = scale_y
    ar_object.scale_z = scale_z
    ar_object.pos_offset_x = pos_x
    ar_object.pos_offset_y = pos_y
    ar_object.pos_offset_z = pos_z
    ar_object.save()


@csrf_exempt
def upload_image_api(request, pk):
    _name = request.POST.get('image_name')
    _scene = Scene.objects.filter(name=pk)
    if _scene.count() == 0:
        return error_json("Scene is not present")
    upload_image(request, _name, _scene[0])
    return success()

@csrf_exempt
def link_image_with_ar_object(request, pk):
    _image_name = request.POST.get('image_name')
    _object_name = request.POST.get('ar_object_name')
    _scene = Scene.objects.filter(name=pk)
    if len(_scene) == 0:
        return error_json("Scene is not present")
    _image_target = Image_target.objects.filter(name=_image_name)[0]
    _ar_object = Ar_object.objects.filter(name=_object_name)[0]
    image_target_ar_object = Image_target_ar_object(scene = _scene[0], image_target = _image_target, ar_object=_ar_object)
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
    ar_object = {"name": link.ar_object.name, "link": ar_object_link,
                 "scale_x" : link.ar_object.scale_x,
                 "scale_y": link.ar_object.scale_y,
                 "model_type": link.ar_object.model_type,
                 "mtl_link": link.ar_object.mtl_link,
                 "scale_z": link.ar_object.scale_z,
                 "rot_x": link.ar_object.rot_x,
                 "rot_z": link.ar_object.rot_z,
                 "pos_offset_x": link.ar_object.pos_offset_x,
                 "pos_offset_y": link.ar_object.pos_offset_y,
                 "pos_offset_z": link.ar_object.pos_offset_z
                 }
    return {"image_target": image_target, "ar_object": ar_object}