from django.shortcuts import render
from app.models import Person

def people(request):
    thead = ['ID', 'NAME']
    tbody = Person.objects.all()
    return render(request, "index.html", {'thead': thead, 'hbody': tbody})

