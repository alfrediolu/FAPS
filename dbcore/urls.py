from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Represents the core URLs for the database. AdminCP is affiliated with the dbcore module and not proteindb.
# Also registers all URLs from proteindb.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('proteindb.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL ,document_root = settings.STATIC_ROOT)
