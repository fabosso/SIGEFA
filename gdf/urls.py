from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # DJANGO APPS URLS
    path('accounts/', include('django.contrib.auth.urls')),

    # LOCAL APPS URLS
    path('', include('apps.ecr.urls', namespace="ecr")),
    path('', include('apps.users.urls', namespace='users')),

    # RESTful API GDF App url's
    path('api/', include('apps.ecr.api.urls')),
    path('api-auth/', include('rest_framework.urls')),

    # ---------> ONLY TEST <----------#
    # path('', include('apps.tests.urls', namespace="tests")), 

]

# if "debug_toolbar" in settings.INSTALLED_APPS:
#     import debug_toolbar
#     urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
