"""
WSGI config for help project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os, sys, site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir(r'C:\Python27\Lib\site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append(r'C:\GitHub\help')
sys.path.append(r'C:\GitHub\help\help')

#print sys.path

from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "help.settings")
application = get_wsgi_application()
