from django.shortcuts import render

# Create your views here.

def verIndex(request):
    return render(request, "index.html")

def verLogin(request):
    return render(request, "login.html")

def registrarMiembro(request):
    return render(request, "registroMiembro.html")