from django.http import HttpRequest, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .forms.client import CreateClientForm, UpdateClientForm
from .models import Client

@login_required
def index(request: HttpRequest):
    return render(request, 'index.html')

@login_required
def create_client(request: HttpRequest):
    if request.method == "POST":
        form = CreateClientForm(request.POST)
        
        if not form.is_valid():
            return render(request, "client/create.html", { "errors": form.errors })
        
        Client(
            name=request.POST["name"], 
            email=request.POST["email"], 
            createdBy=request.user
        ).save()
        messages.success(request, "Client created")
        
        return HttpResponseRedirect(reverse("clients"))
    
    else:
        return render(request, "client/create.html", { "form": CreateClientForm() })

@require_http_methods(["POST"])
def update_client(request: HttpRequest, pk: int):
    form = UpdateClientForm(request.POST)
    
    if not form.is_valid():
        messages.error(request, "The submitted form had errors.")
        return HttpResponseRedirect(reverse("clients"))
        
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        raise Http404("No client matches the given query.") 
    
    client.name = form.cleaned_data['name'] 
    client.email = form.cleaned_data['email']
    client.active = request.POST['active'] == "1" # Convert value to boolean
    client.save()
    
    messages.success(request, "Client details updated.")
    
    return HttpResponseRedirect(reverse("clients"))
    

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    
    def get_queryset(self):
        return (Client.objects
                     .filter(deleted__exact=False)
                     .order_by("-createdAt"))
    

