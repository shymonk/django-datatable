from django.shortcuts import render
from app.models import Person

def people(request):
    table = {}
    table['name'] = 'people'
    table['thead'] = [u'序号', u'姓名']
    table['tbody'] = Person.objects.all()
    return render(request, "index.html", {'people': table})

