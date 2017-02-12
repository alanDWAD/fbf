from settings import *

DEBUG = False
ALLOWED_HOSTS = [] if DEBUG else ['test.dwad.org']
DATABASES = {'default': {'ENGINE': 'django.db.backends.mysql',
                         'NAME': 'dwad_demo',
                         'USER': 'dwad',
                         'PASSWORD': '7LWo1SXqdJF69PL'}}

PAYPAL_SANDBOX = True
PAYPAL_EMAIL = 'dan@dwad.org' # Sandbox account
