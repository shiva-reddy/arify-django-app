"""arify_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from arify_app import views
from arify_app.views import scenes_list, scene_links, upload_image, link_image_with_ar_object, list_ar_objects, \
    list_image_targets

urlpatterns = [

    path('', views.index, name='index'),
    path('add_scene/', views.add_scene, name='add_scene'),
    path("scenes/", scenes_list, name="scenes_list"),
    path("scenes/<str:pk>/list_links", scene_links, name="scene_links"),
    path("scenes/<str:pk>/list_image_targets", list_image_targets, name="list_image_targets"),
    path("scenes/<str:pk>/list_ar_objects", list_ar_objects, name="list_ar_objects"),
    path("scenes/<str:pk>/upload_image", upload_image, name="upload_image"),
    path("scenes/<str:pk>/link_image_with_ar_object", link_image_with_ar_object, name="link_image_with_ar_object"),
    path('add_ar_object/', views.add_ar_object, name='add_ar_object'),
    path('admin/', admin.site.urls),
]
