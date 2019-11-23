from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('insert_new_form', views.insert_new_form),
    path('delete_new_form', views.delete_new_form),
    path('upadte_new_form', views.upadte_new_form),
    path('enable_disable', views.enable_disable),
    path('badges_data_retrival', views.badges_data_retrival),
    path('retriving_data', views.retriving_data),
    path('log_data_retrival', views.log_data_retrival),
    path('approval_data_dropdown', views.approval_data_dropdown),
    path('Business_type_data_dropdown', views.Business_type_data_dropdown),
    path('SAP_data_dropdown', views.SAP_data_dropdown),
    path('PO_data_dropdown', views.PO_data_dropdown),
    path('Indent_data_dropdown', views.Indent_data_dropdown),
    path('Requirement_data_dropdown', views.Requirement_data_dropdown),
    path('plants_drop_down', views.plants_drop_down),
    path('C_P_Received_by_dropdown', views.C_P_Received_by_dropdown),
    path('yes_no_data_dropdown', views.yes_no_data_dropdown),
    path('dummy_insert', views.dummy_insert),
]
