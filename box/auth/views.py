from django.http import HttpResponse

def login(request):
    return HttpResponse("HELLO WORLD!")