from django.shortcuts import render, get_object_or_404
from apps.cars.models import Car, CarModel, CarType

def home(request):
    return render(request, 'core/home.html')

def car_list(request):
    # Get all unique car models
    car_models = CarModel.objects.all()
    return render(request, 'cars/car_page.html', {'car_models': car_models})

def cars_by_model(request, car_model_id):
    car_model = get_object_or_404(CarModel, id=car_model_id)
    
    # Get all cars for this model, including car_image
    cars = Car.objects.select_related('car_model', 'car_type', 'driver').filter(
        car_model=car_model
    )
    
    # Get all car types for filtering
    car_types = CarType.objects.all()
    
    return render(request, 'cars/cars_by_model.html', {
        'car_model': car_model,
        'cars': cars,
        'car_types': car_types
    })

def car_detail(request, car_id):
    return render(request, 'cars/car_detail.html')

def cars_category_all(request):
    # Get all cars with their related models and types
    cars = Car.objects.select_related('car_model', 'car_type', 'driver').all()
    
    # Group cars by model
    cars_by_model = {}
    for car in cars:
        model_name = car.car_model.name
        if model_name not in cars_by_model:
            cars_by_model[model_name] = {
                'model': car.car_model,
                'cars': []
            }
        cars_by_model[model_name]['cars'].append(car)
    
    return render(request, 'cars/cars_by_category.html', {
        'cars_by_model': cars_by_model
    })

def cars_by_type(request, car_type):
    # Get all cars filtered by type
    if car_type == 'All':
        cars = Car.objects.select_related('car_model', 'car_type', 'driver').all()
    else:
        if car_type == 'AC':
            # For AC, show AC cars and Both cars
            cars = Car.objects.select_related('car_model', 'car_type', 'driver').filter(
                car_type__name__in=['AC', 'Both']
            )
        elif car_type == 'Non-AC':
            # For Non-AC, show Non-AC cars and Both cars
            cars = Car.objects.select_related('car_model', 'car_type', 'driver').filter(
                car_type__name__in=['Non-AC', 'Both']
            )
        else:
            cars = Car.objects.select_related('car_model', 'car_type', 'driver').filter(
                car_type__name=car_type
            )
    
    # Get all car types for filtering
    car_types = CarType.objects.all()
    
    # Group cars by model
    cars_by_model = {}
    for car in cars:
        model_name = car.car_model.name
        if model_name not in cars_by_model:
            cars_by_model[model_name] = {
                'model': car.car_model,
                'cars': []
            }
        cars_by_model[model_name]['cars'].append(car)
    
    return render(request, 'cars/cars_by_category.html', {
        'cars_by_model': cars_by_model,
        'car_types': car_types,
        'selected_type': car_type
    })