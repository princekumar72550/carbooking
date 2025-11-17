# Car Booking System

A Django-based car booking platform with RESTful APIs for managing car rentals and bookings.

## Features

- Public users can view all cars and filter by category
- Registered users can book cars with JWT authentication
- Admin panel for managing cars, categories, drivers, and bookings
- RESTful API architecture

## Project Structure

```
car_booking_project/
├── car_booking_project/     # Main project settings
├── apps/
│   ├── core/               # Main pages and templates
│   ├── cars/               # Car models, APIs, and administration
│   ├── booking/            # Booking engine and payment handling
│   └── users/              # User accounts and authentication
├── static/                 # CSS, JavaScript, and images
├── media/                  # Car images, driver photos
└── templates/              # Base templates
```

## Setup Instructions

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   ```bash
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Car APIs
- `GET /api/cars/cars/` - List all cars
- `GET /api/cars/cars/<id>/` - Get car details

### Authentication APIs (JWT)
- `POST /api/users/auth/register/` - User registration
- `POST /api/users/auth/login/` - User login

### Booking APIs
- `POST /api/booking/booking/` - Create a booking (login required)
- `GET /api/booking/booking/my/` - Get user's bookings (login required)

## Environment Variables

The project uses a `.env` file for configuration. Key variables include:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `RAZORPAY_KEY_ID` - Razorpay key ID (dummy)
- `RAZORPAY_KEY_SECRET` - Razorpay key secret (dummy)
- `STRIPE_PUBLISHABLE_KEY` - Stripe publishable key (dummy)
- `STRIPE_SECRET_KEY` - Stripe secret key (dummy)

## Deployment

### Render.com Deployment

1. Fork this repository to your GitHub account
2. Create a new Web Service on Render
3. Connect your forked repository
4. Set the following environment variables in Render:
   - `SECRET_KEY` - A secure random string
   - `DEBUG` - False
   - `ALLOWED_HOSTS` - Your Render app URL (e.g., your-app-name.onrender.com)
5. The build process will automatically:
   - Install dependencies
   - Collect static files
   - Apply database migrations
6. Your app will be available at https://your-app-name.onrender.com

## Frontend Pages

- `/` - Home page
- `/cars/` - Car listing page
- `/car/<id>/` - Car details page
- `/login/` - Login page
- `/register/` - Registration page
- `/booking/` - Booking page

All frontend pages use JavaScript fetch() to call the APIs.