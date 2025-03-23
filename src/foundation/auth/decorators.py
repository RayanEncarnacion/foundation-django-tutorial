from django.http import Http404
from functools import wraps
from django.shortcuts import get_object_or_404

def user_owns_resource(model):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            resource = get_object_or_404(model, pk=kwargs.get('pk'))
            
            if request.user != resource.createdBy:
                raise  Http404("You do not have permission to access this resource.")
            
            return func(request, *args, **kwargs)
        
        return inner
    
    return decorator
