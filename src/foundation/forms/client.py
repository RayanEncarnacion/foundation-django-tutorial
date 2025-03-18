from django import forms
from ..models import Client

def get_active_clients():
    return Client.objects.filter(active__exact=True, deleted__exact=False)

class CreateClientForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, strip=True)
    email = forms.EmailField(required=True)
    
class UpdateClientForm(CreateClientForm):
    active = forms.BooleanField(required=True)