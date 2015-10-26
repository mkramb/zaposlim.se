from django.conf import settings

def site(request):
    return {
        'PROJECT_URL' : settings.PROJECT_URL
    }
