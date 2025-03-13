from django.http import HttpResponse, HttpRequest

def index(_: HttpRequest):
    return HttpResponse('<h1>Hello world!</h1>')