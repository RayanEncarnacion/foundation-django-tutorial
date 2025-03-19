from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'foundation'

urlpatterns = [
    path('', views.index, name="index"),
    path('create/client', views.create_client, name="create_client"),
    path('client/<int:pk>/update', views.update_client, name="update_client"),
    path('client/<int:pk>/delete', views.delete_client, name="delete_client"),
    path('clients', 
         views.ClientListView.as_view(template_name="client/list.html"), name="clients"),
    
    # Auth views
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    
    path('admin/', admin.site.urls),
]


""" if settings.DEBUG:
    import debug_toolbar
    
    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls))) """