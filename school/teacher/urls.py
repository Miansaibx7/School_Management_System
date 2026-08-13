from django.urls import path

from . import views

urlpatterns = [
    # ===================== TEACHER URLS =====================
    path("teachers/", views.teacher_list, name="teacher_list"),
    path("teachers/create/", views.teacher_create, name="teacher_create"),
    path("teachers/update/<int:pk>/", views.teacher_update, name="teacher_update"),
    path("teachers/delete/<int:pk>/", views.teacher_delete, name="teacher_delete"),
]

