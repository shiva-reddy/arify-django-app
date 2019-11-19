from django import forms

class SceneNameForm(forms.Form):
    scene_name = forms.CharField(label='Scene Name', max_length=100, required=True)

class ARObjectForm(forms.Form):
    object_name = forms.CharField(label='AR Object name', max_length=100, required=True)
    chosen_scene = forms.ChoiceField(label='Scene Name', required=True)
    file = forms.FileField(label='Upload your object', required=True)

class UploadForm(forms.Form):
    file = forms.FileField()