from django.urls import path
from . import views

app_name = 'myapp'
urlpatterns = [
    path('', views.drug_list, name='drug_list'),
    path('json/', views.drug_list_json, name='drug_list_json'),
    path('drug/details/<int:drug_id>/', views.get_drug_details, name='drug_details'),
]