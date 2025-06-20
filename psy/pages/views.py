from django.http import HttpResponse


def index(request):
    return HttpResponse("Меня зовут Мария О., я психолог.")
