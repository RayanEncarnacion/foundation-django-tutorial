from django.http import HttpRequest, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .models import Client, Project
from .forms.project import CreateProjectForm, UpdateProjectForm
from .forms.client import CreateClientForm, UpdateClientForm

@login_required
def index(request: HttpRequest):
    context = {
        'clients_count': Client.objects.filter(deleted__exact=False).count(),
        'projects_count': Project.objects.filter(deleted__exact=False).count()
    }
    return render(request, 'index.html', context)

@login_required
def create_client(request: HttpRequest):
    if request.method == "POST":
        form = CreateClientForm(request.POST)
        
        if not form.is_valid():
            return render(request, "client/create.html", { "errors": form.errors })
        
        Client(createdBy=request.user, **form.cleaned_data).save()
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
    client.active = request.POST['active'] == "1"
    client.save()
    
    messages.success(request, "Client details updated.")
    
    return HttpResponseRedirect(reverse("clients"))

@require_http_methods(["POST"])
def delete_client(request: HttpRequest, pk: int):
    client = get_object_or_404(Client, pk=pk)
    client.delete()
    
    messages.success(request, "Client deleted successfully.")
    
    return HttpResponseRedirect(reverse("clients"))

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    
    def get_queryset(self):
        return (Client.objects
                     .filter(deleted__exact=False)
                     .order_by("-createdAt"))
        
## Projects views
@login_required
def create_project(request: HttpRequest):
    if request.method == "POST":
        form = CreateProjectForm(request.POST)
        
        if not form.is_valid():
            return render(request, "project/create.html", { "form": form, "errors": form.errors })
        
        Project(createdBy = request.user, **form.cleaned_data).save()
        messages.success(request, "Project created")
        
        return HttpResponseRedirect(reverse("projects"))
    
    else:
        form = CreateProjectForm()
        return render(request, "project/create.html", { "form": form })

@require_http_methods(["POST"])
def delete_project(request: HttpRequest, pk: int):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    
    messages.success(request, "Project deleted successfully.")
    
    return HttpResponseRedirect(reverse("projects"))
 
class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name="project/list.html"       
    
    def get_queryset(self):
        return (Project.objects.select_related("client")
                               .filter(deleted__exact=False)
                               .order_by("-createdAt"))
        
    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['clients'] = Client.objects.all()
        
        return context
        
@require_http_methods(["POST"])
def update_project(request: HttpRequest, pk: int):
    form = UpdateProjectForm(request.POST)
    
    if not form.is_valid():
        print(form.errors)
        messages.error(request, "The submitted form had errors.")
        return HttpResponseRedirect(reverse("projects"))
        
    project = get_object_or_404(Project, pk=pk)
    project.name = form.cleaned_data['name'] 
    project.amount = form.cleaned_data['amount']
    project.client = form.cleaned_data['client']
    project.active = request.POST['active'] == "1"
    project.save()
    
    messages.success(request, "Project details updated.")
    
    return HttpResponseRedirect(reverse("projects"))
