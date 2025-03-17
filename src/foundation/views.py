from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


from .forms.client import CreateClient
from .models import Client

def index(request: HttpRequest):
    return render(request, 'index.html')

@login_required
def create_client(request: HttpRequest):
    if request.method == "POST":
        form = CreateClient(request.POST)
        
        if not form.is_valid():
            return render(request, "client/create.html", { "errors": form.errors })
        
        Client(
            name=request.POST["name"], 
            email=request.POST["email"], 
            createdBy=request.user
        ).save()
        
        return HttpResponseRedirect(reverse("clients"))
    
    else:
        return render(request, "client/create.html", { "form": CreateClient() })



class ClientListView(LoginRequiredMixin, ListView):
    model = Client

