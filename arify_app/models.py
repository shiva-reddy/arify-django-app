from django.db import models

# Create your models here.
class Scene(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Ar_object(models.Model):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.name

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
