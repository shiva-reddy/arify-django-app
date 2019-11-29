from django.db import models

# Create your models here.
class Scene(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def add_scene(scene_name):
        s = Scene(name=scene_name)
        s.save()

class Ar_object(models.Model):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    model_type = models.CharField(max_length=200, default="OBJ")
    mtl_link = models.CharField(max_length=200,default=None, blank=True, null=True)
    scale_x = models.DecimalField(decimal_places=2, max_digits= 3, default=1.0)
    scale_y = models.DecimalField(decimal_places=2, max_digits= 3, default=1.0)
    scale_z = models.DecimalField(decimal_places=2, max_digits= 3, default=1.0)
    pos_offset_x = models.DecimalField(decimal_places=2, max_digits=3, default=0.0)
    pos_offset_y = models.DecimalField(decimal_places=2, max_digits=3, default=0.0)
    pos_offset_z = models.DecimalField(decimal_places=2, max_digits=3, default=0.0)
    rot_x = models.DecimalField(decimal_places=2, max_digits= 3, default=0.0)
    rot_y = models.DecimalField(decimal_places=2, max_digits= 3, default=0.0)
    rot_z = models.DecimalField(decimal_places=2, max_digits= 3, default=0.0)

    def __str__(self):
        return self.name

    def add_object(chosen_scene, object_name, file_link, _mtl_link, _model_type, _scale_x, _scale_y, _scale_z, _rot_x,
                   _rot_y, _rot_z, _pos_offset_x, _pos_offset_y, _pos_offset_z):
        _scene = Scene.objects.filter(name=chosen_scene).last()
        obj = Ar_object(scene = _scene,
                        name= object_name,
                        link=file_link,
                        mtl_link = _mtl_link,
                        model_type = _model_type,
                        scale_x = _scale_x,
                        scale_y = _scale_y,
                        scale_z = _scale_z,
                        rot_x = _rot_x,
                        rot_y=_rot_y,
                        rot_z=_rot_z,
                        pos_offset_x = _pos_offset_x,
                        pos_offset_y=_pos_offset_y,
                        pos_offset_z=_pos_offset_z)
        obj.save()

class Image_target(models.Model):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Image_target_ar_object(models.Model):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE)
    image_target = models.ForeignKey(Image_target, on_delete=models.CASCADE)
    ar_object = models.ForeignKey(Ar_object, on_delete=models.CASCADE)
