from django.http import HttpRequest, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from foundation.models import Client, Project
from foundation.forms.project import CreateProjectForm, UpdateProjectForm
from foundation.forms.client import CreateClientForm, UpdateClientForm
from foundation.auth.decorators import user_owns_resource

@login_required
def index(request: HttpRequest):
    context = {
        'clients_count': Client.objects.filter(deleted__exact=False, createdBy = request.user).count(),
        'projects_count': Project.objects.filter(deleted__exact=False, createdBy = request.user).count()
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
@user_owns_resource(Client)
def update_client(request: HttpRequest, pk: int):
    client = get_object_or_404(Client, pk=pk)
    
    if not client.createdBy == request.user:
        HttpResponseForbidden()
        
    form = UpdateClientForm(request.POST)
    
    if not form.is_valid():
        messages.error(request, "The submitted form had errors.")
        return HttpResponseRedirect(reverse("clients"))
        
    client.name = form.cleaned_data['name'] 
    client.email = form.cleaned_data['email']
    client.active = request.POST['active'] == "1"
    client.save()
    
    messages.success(request, "Client details updated.")
    
    return HttpResponseRedirect(reverse("clients"))

@require_http_methods(["POST"])
@user_owns_resource(Client)
def delete_client(request: HttpRequest, pk: int):
    client = get_object_or_404(Client, pk=pk)
    client.delete()
    
    messages.success(request, "Client deleted successfully.")
    
    return HttpResponseRedirect(reverse("clients"))

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name="client/list.html"
    
    def get_queryset(self):
        return (Client.objects
                     .filter(deleted__exact=False, createdBy = self.request.user))

@login_required
def client_projects(request, pk):
    client = get_object_or_404(Client, pk=pk)
    
    context = {
        "client": client,
        "projects": client.projects.filter(deleted__exact=False)
    }
    
    return render(request, "client/projects.html", context)
        
## Projects views
@login_required
def create_project(request: HttpRequest):
    if request.method == "POST":
        form = CreateProjectForm(request.POST)
        
        if not form.is_valid():
            return render(request, "project/create.html", { "form": form, "errors": form.errors })
        
        Project(createdBy = request.user, **form.cleaned_data).save()
        messages.success(request, "Project created")
        
        return HttpResponseRedirect(request.path_info)
    
    else:
        client_id = request.GET.get('client')
        
        if client_id:
            get_object_or_404(Client, pk=client_id)
            
        form = CreateProjectForm(initial={ 'client': client_id })
        
        return render(request, "project/create.html", { "form": form })

@require_http_methods(["POST"])
@user_owns_resource(Project)
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
                               .filter(deleted__exact=False, createdBy = self.request.user))
        
    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['clients'] = Client.objects.all()
        
        return context

@require_http_methods(["POST"])
@user_owns_resource(Project)
def update_project(request: HttpRequest, pk: int):
    project = get_object_or_404(Project, pk=pk)
    form = UpdateProjectForm(request.POST, instance=project)
    
    if not form.is_valid():
        messages.error(request, "The submitted form had errors.")
        return HttpResponseRedirect(reverse("projects"))
        
    project.name = form.cleaned_data['name'] 
    project.amount = form.cleaned_data['amount']
    project.client = form.cleaned_data['client']
    project.active = request.POST['active'] == "1"
    project.save()
    
    messages.success(request, "Project details updated.")
    
    return HttpResponseRedirect(reverse("projects"))
