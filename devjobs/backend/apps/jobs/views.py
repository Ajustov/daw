from django.conf import settings
from django.shortcuts import render


def home(request):
  frontend_url = settings.CORS_ALLOWED_ORIGINS[0]
  return render(request, 'index.html', {'frontend_url': frontend_url})
