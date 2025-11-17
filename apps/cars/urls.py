from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cars/', views.car_list, name='car_list'),
    path('cars/category/', views.cars_category_all, name='cars_category_all'),
    path('cars/category/<int:car_model_id>/', views.cars_by_model, name='cars_by_model'),
    path('cars/type/<str:car_type>/', views.cars_by_type, name='cars_by_type'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
]