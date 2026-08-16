from django.urls import path
from . import views

urlpatterns = [
    # ===================== Sudents URLS =====================
    path("students/", views.student_list, name="student_list"),
    path("students/create/", views.student_create, name="student_create"),
    path("students/update/<int:pk>/", views.student_update, name="student_update"),
    path("students/delete/<int:pk>/", views.student_delete, name="student_delete"),
]

from django.conf import settings
from django.conf.urls.static import static

# This is REQUIRED to show photos during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
