from django.urls import path
from . import api_views

urlpatterns = [
    # Category URLs
    path('categories/', api_views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', api_views.CategoryDetailView.as_view(), name='category-detail'),
    
    # Driver URLs
    path('drivers/', api_views.DriverListCreateView.as_view(), name='driver-list-create'),
    path('drivers/<int:pk>/', api_views.DriverDetailView.as_view(), name='driver-detail'),
    
    # Car URLs
    path('cars/', api_views.CarListCreateView.as_view(), name='car-list-create'),
    path('cars/<int:pk>/', api_views.CarDetailView.as_view(), name='car-detail'),
]