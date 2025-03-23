from django import forms
from ..models import Client, Project

from django.forms import ModelForm

default_field_classes = 'bg-gray-50 border border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 mb-2'

def get_active_clients():
    return Client.objects.filter(active__exact=True, deleted__exact=False)

class CreateProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["name", "amount", "client"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs.update({ "class": default_field_classes })
            
class UpdateProjectForm(CreateProjectForm):
    active = forms.BooleanField(required=True)