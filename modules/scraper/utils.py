from django.core.management import setup_environ
import imp

def setup_django_env(path):
    f, filename, desc = imp.find_module('settings', [path])
    project = imp.load_module('settings', f, filename, desc)

    setup_environ(project)
