from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('accounts/', include('accounts.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]

# First installed the django_browser_reload package using pip install django-browser-reload. or uv add django-browser-reload
# Then added 'django_browser_reload' to the INSTALLED_APPS list in settings.py.
# After that, Included the BrowserReloadMiddleware in the MIDDLEWARE list. 
# Finally, I added the URL pattern for django_browser_reload in urls.py.