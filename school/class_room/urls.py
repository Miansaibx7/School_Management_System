from django.urls import path
from . import views

urlpatterns = [
    # ===================== CLASS URLS =====================
    path("classes/", views.class_list, name="class_list"),
    path("classes/create/", views.class_create, name="class_create"),
    path("classes/update/<int:pk>/", views.class_update, name="class_update"),
    path("classes/delete/<int:pk>/", views.class_delete, name="class_delete")
]

