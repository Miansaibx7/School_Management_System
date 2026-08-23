from django.urls import path
from . import views

urlpatterns = [
    # ===================== Fees URLS ====================================
    path("fees/", views.fee_list, name="fee_list"),
    path("fees/create/", views.fee_create, name="fee_create"),
    path("fees/update/<int:pk>/", views.fee_update, name="fee_update"),
    path("fees/delete/<int:pk>/", views.fee_delete, name="fee_delete"), 
]
