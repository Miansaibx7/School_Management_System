from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path("__reload__/", include("django_browser_reload.urls")), # django-browser-reload url 
]

# First install uv add --dev django-browser-reload
# Second add django_browser_reload to installed apps
# Third add the django_browser_reload url
# Four add django_browser_reload.middleware.BrowserReloadMiddleware to middleware