from django.urls import include, path

from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    # ===================== Fees URLS ====================================
    path("fees/", views.fee_list, name="fee_list"),
    path("fees/create/", views.fee_create, name="fee_create"),
    path("fees/update/<int:pk>/", views.fee_update, name="fee_update"),
    path("fees/delete/<int:pk>/", views.fee_delete, name="fee_delete"),
    # ===================== Salary URLS ====================================
    path("salaries/", views.salary_list, name="salary_list"),
    path("salaries/create/", views.salary_create, name="salary_create"),
    path("salaries/update/<int:pk>/", views.salary_update, name="salary_update"),
    path("salaries/delete/<int:pk>/", views.salary_delete, name="salary_delete"),
    # ===================== Financial Reports URLS ====================================
    path("financial-reports/", views.financial_reports, name="financial_reports"),

    # Include accounts app (authentication + user management)
    path("", include("accounts.urls")),

    # Include teacher app (teacher management)
    path("", include("teacher.urls")),

    # Include class_room app (class_room Management)
    path("", include("class_room.urls")),

    # Include section app (section Management)
    path("", include("section.urls")),

    # Include student app (student Management)
    path("", include("students.urls")),

    # Include transaction app (transaction Management)
    path("", include("transaction.urls")),
    
]

from django.conf import settings
from django.conf.urls.static import static

# This is REQUIRED to show photos during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
