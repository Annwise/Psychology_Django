from django.shortcuts import render


def home(request):
    return render(request, 'pages/home.html')


def blog(request):
    return render(request, 'pages/blog.html')


def docs(request):
    return render(request, 'pages/docs.html')
