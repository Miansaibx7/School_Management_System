from django.urls import path
from . import views

urlpatterns = [
    # ===================== Sections URLS =====================
    path("sections/", views.section_list, name="section_list"),
    path("sections/create/", views.section_create, name="section_create"),
    path("sections/update/<int:pk>/", views.section_update, name="section_update"),
    path("sections/delete/<int:pk>/", views.section_delete, name="section_delete"),
]

