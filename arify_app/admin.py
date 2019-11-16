from django.contrib import admin

from .models import Scene,Image_target,Ar_object,Image_target_ar_object

admin.site.register(Scene)
admin.site.register(Image_target)
admin.site.register(Ar_object)
admin.site.register(Image_target_ar_object)
