from django import forms
from ..models import Client, Project

default_field_classes = 'bg-gray-50 border border-gray-600 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 mb-2'

class CreateProjectForm(forms.ModelForm):    
    payDays = forms.MultipleChoiceField(
        label='Pay day(s)',
        choices=[(i, i) for i in range(1, 31)],
        widget=forms.SelectMultiple(attrs={'class': default_field_classes})
    )
    
    class Meta:
        model = Project
        fields = ["name", "amount", "client", 'payDays']
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs.update({ "class": default_field_classes })
            
        if self.user:
            self.fields['client'].queryset = Client.objects.filter(active__exact=True, 
                                                                   deleted__exact=False, 
                                                                   createdBy=self.user)

class UpdateProjectForm(CreateProjectForm):
    active = forms.BooleanField(required=True)