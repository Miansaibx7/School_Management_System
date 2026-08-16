from django.urls import path
from . import views

urlpatterns = [
    # ===================== Sudents URLS =====================
    path("students/", views.student_list, name="student_list"),
    path("students/create/", views.student_create, name="student_create"),
    path("students/update/<int:pk>/", views.student_update, name="student_update"),
    path("students/delete/<int:pk>/", views.student_delete, name="student_delete"),
]

