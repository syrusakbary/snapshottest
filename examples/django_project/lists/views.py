from django.shortcuts import redirect, render
from lists.models import List


def home_page(request):
    lists = List.objects.all()
    return render(request, 'home.html', {'lists': lists})