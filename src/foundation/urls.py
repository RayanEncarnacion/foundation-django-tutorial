from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'foundation'

urlpatterns = [
    path('', views.index, name="index"),
    
    # Client views
    path('client/create', views.create_client, name="create_client"),
    path('client/<int:pk>/update', views.update_client, name="update_client"),
    path('client/<int:pk>/delete', views.delete_client, name="delete_client"),
    path('client/<int:pk>/projects', views.ClientProjectsListView.as_view(), name="client_projects"),
    path('clients', views.ClientListView.as_view(), name="clients"),
    
    # Project views
    path('project/create', views.create_project, name="create_project"),
    path('project/<int:pk>/update', views.update_project, name="update_project"),
    path('project/<int:pk>/delete', views.delete_project, name="delete_project"),
    path('projects', views.ProjectListView.as_view(), name="projects"),
    
    # Auth views
    path("login/", auth_views.LoginView.as_view(template_name="login.html", redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    
    # Admin views
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    
    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))