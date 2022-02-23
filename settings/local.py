from .base import *


DEBUG = True


ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# SQLITE3

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': (BASE_DIR / 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
	os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# DEBUG TOOLBAR PANELS SETTINGS
# if DEBUG:
#     INSTALLED_APPS.append("debug_toolbar")


# if "debug_toolbar" in INSTALLED_APPS:
#     DEBUG_TOOLBAR_PANELS = [
#         'debug_toolbar.panels.versions.VersionsPanel',
#         'debug_toolbar.panels.timer.TimerPanel',
#         'debug_toolbar.panels.settings.SettingsPanel',
#         'debug_toolbar.panels.headers.HeadersPanel',
#         'debug_toolbar.panels.request.RequestPanel',
#         'debug_toolbar.panels.sql.SQLPanel',
#         'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#         'debug_toolbar.panels.templates.TemplatesPanel',
#         'debug_toolbar.panels.cache.CachePanel',
#         'debug_toolbar.panels.signals.SignalsPanel',
#         'debug_toolbar.panels.logging.LoggingPanel',
#         'debug_toolbar.panels.redirects.RedirectsPanel',
#         'debug_toolbar.panels.profiling.ProfilingPanel',
#     ]

#     def show_toolbar(request):
#         return True

#     DEBUG_TOOLBAR_CONFIG = {
#         'INTERCEPT_REDIRECTS': False,
#         'SHOW_TOOLBAR_CALLBACK': show_toolbar
#     }
