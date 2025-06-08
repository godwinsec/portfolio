from django.shortcuts import render
from django.http import FileResponse
import os
from django.conf import settings

# Create your views here.

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def view_cv(request):
    file_path = os.path.join(settings.STATICFILES_DIRS[0], 'files', 'GCV-june.pdf')
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
