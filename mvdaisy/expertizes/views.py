
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse




def index(request):
	context = {"listik": [1,2,3,4,5,6,7], "active": "expertizes"}
	return render(request, "expertizes/index.html", context=context)