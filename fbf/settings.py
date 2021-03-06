from django.contrib import messages
import os.path
import socket

# If the host name is not dwad.org then run in debug mode.
DEBUG = socket.gethostname() != 'str8red.com'

# Site settings.
ADMINS = (('Alan Tingey', 'alan.tingey@bakkavor.com'),)
MANAGERS = (('Alan Tingey', 'alan@dwad.org'), ('Alan Tingey', 'alan@dwad.org'))
DEFAULT_FROM_EMAIL = 'str8red.org <noreply@str8red.org>'
SERVER_EMAIL = DEFAULT_FROM_EMAIL
SECRET_KEY = '&4opo0bb)%z$lxu=7@qva$l95%74j!l!bpfhj5393*o)z6s&+1'
ALLOWED_HOSTS = [] if DEBUG else ['str8red.com']
DATABASES = {'default': {'ENGINE': 'django.db.backends.mysql',
                         'NAME': 'fbf',
                         'USER': 'fbfuser',
                         'PASSWORD': 'Ammo1979kmf'}}
CONN_MAX_AGE = 0 if DEBUG else 21600 # 6-hour keep-alive (must be <= MySQL's default of 8 hours)
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
                      'LOCATION': 'cache'}}

# Locale/iternationalisation
TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'
USE_I18N = False
USE_L10N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/str8red.com/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_URL = '/resources/'
MEDIA_ROOT = 'media' if DEBUG else '/var/www/str8red.com/resources/'


# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.dirname(__file__), 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {'debug': DEBUG,
                    'context_processors': [
                        'django.contrib.auth.context_processors.auth',
                        'django.template.context_processors.debug',
                        'django.template.context_processors.media',
                        'django.template.context_processors.static',
                        'django.template.context_processors.tz',
                        'django.contrib.messages.context_processors.messages',
			'django.template.context_processors.request',
                    ]},
    }
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
)

# URLs
ROOT_URLCONF = 'fbf.urls'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_URL = 'logout'

# Middleware
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
if DEBUG: MIDDLEWARE_CLASSES += ('fbf.middleware.QueryCountDebugMiddleware',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sites',  
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    # Third-party apps
    'avatar',
    'mathfilters',
    'smart_selects',
    'tinymce',
    'dbbackup',
    'django_ical',
    'crispy_forms',
    'phonenumber_field',
    # DWAD apps
    'meta',
)

SITE_ID = 4

# Messages
MESSAGE_TAGS = {messages.DEBUG: 'alert alert-info',
                messages.INFO: 'alert alert-info',
                messages.SUCCESS: 'alert alert-success',
                messages.WARNING: 'alert alert-warning',
                messages.ERROR: 'alert alert-danger'}

# Avatars
AVATAR_MAX_AVATARS_PER_USER = 1
AUTO_GENERATE_AVATAR_SIZES = [64, 92, 200]
AVATAR_GRAVATAR_BACKUP = False
AVATAR_DEFAULT_URL = 'default-avatar-red.png'

# TinyMCE configuration
TINYMCE_DEFAULT_CONFIG = {'theme': 'advanced',
                          'convert_urls': False,
                          'relative_urls': False,
                          'plugins': 'paste,autoresize',
                          'width': '100%',
                          'paste_text_sticky': True,
                          'paste_text_sticky_default': True,
                          'paste_text_linebreaktype': 'p',
                          'content_css': '/static/tinymce.css',
                          'theme_advanced_resizing': True,
                          'theme_advanced_buttons1': 'bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,|,bullist,numlist,|,outdent,indent,|,link,unlink,|,sub,sup,charmap,|,undo,redo,|,cleanup,code'}

PAYPAL_SANDBOX = DEBUG
PAYPAL_EMAIL = 'dan@dwad.org' if PAYPAL_SANDBOX else 'paypal@dwad.org'

# Send 500 errors to admins and log DB request counts in DEBUG mode.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {'level': 'ERROR', 'filters': ['require_debug_false'], 'class': 'django.utils.log.AdminEmailHandler'},
        'console': {'level': 'DEBUG', 'class': 'logging.StreamHandler'},
    },
    'filters': {'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}},
    'loggers': {
        'django.request': {'handlers': ['mail_admins'], 'level': 'ERROR', 'propagate': True},
        'fbf.middleware': {'handlers': ['console'], 'level': 'DEBUG'},
    }
}

# Tests
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Back-up
DBBACKUP_STORAGE = 'dbbackup.storage.dropbox_storage'
DBBACKUP_TOKENS_FILEPATH = '.dropbox'
DBBACKUP_DROPBOX_APP_KEY = 'gauknvdolkjqpkv'
DBBACKUP_DROPBOX_APP_SECRET = 'cav76c0d0mgc09r'
DBBACKUP_DROPBOX_ACCESS_TYPE = 'app_folder'

# Mailchimp
MAILCHIMP_API_KEY = 'f76a01ca08dd48f5bb0b3e85011acc63-us3'
MAILCHIMP_LIST_ID = '5fda30b329'

# Twitter
TWITTER_CONSUMER_KEY = None if DEBUG else 'VhVb8kulUHmQD2RDM0JQgfeZF'
TWITTER_CONSUMER_SECRET = None if DEBUG else 'F0VcyozxU9J0ylwOhVzy8kl1E5OEKXclpEniAgsOnZPuSlGUYO'
TWITTER_ACCESS_TOKEN = None if DEBUG else '1664744718-Rav7PaspvFRNr44WqTEjIhjK1J3hRrAmN3is64o'
TWITTER_ACCESS_TOKEN_SECRET = None if DEBUG else 'WU2ZjXB07rU10l5h3zE2TK2Xj2vmGMaC1m0Z73FF1Q5Oo'

#Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap3'
