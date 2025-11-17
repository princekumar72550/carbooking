// Display cars in the car list
function displayCars(cars) {
    const carList = document.getElementById('car-list') || document.getElementById('car-listings');
    if (!carList) return;
    
    if (!cars || cars.length === 0) {
        showNoResults(true);
        return;
    }
    
    showNoResults(false);
    
    let carsHtml = '';
    cars.forEach(car => {
        carsHtml += `
            <div class="col-4">
                <div class="card car-card">
                    ${car.car_image ? 
                        `<img src="${car.car_image}" class="card-img-top car-image" alt="${car.name}">` : 
                        `<div class="card-img-top car-image bg-light d-flex align-items-center justify-content-center">
                            <i class="bi bi-car-front-fill text-muted" style="font-size: 3rem;"></i>
                        </div>`
                    }
                    <div class="card-body">
                        <h5 class="card-title">${car.name}</h5>
                        <p class="card-text">
                            <span class="badge bg-primary">${car.category_name}</span>
                        </p>
                        <p class="card-text">
                            <strong>Driver:</strong> ${car.driver_name}
                        </p>
                        <p class="card-text car-price">
                            ₹${car.price_per_km}/km
                        </p>
                        <p class="card-text">
                            <span class="availability-indicator ${car.is_available ? 'available' : 'not-available'}"></span>
                            ${car.is_available ? 'Available' : 'Not Available'}
                        </p>
                        <a href="/car/${car.id}/" class="btn btn-primary">
                            <i class="bi bi-eye"></i> View Details
                        </a>
                    </div>
                </div>
            </div>
        `;
    });
    
    carList.innerHTML = carsHtml;
}

function showNoResults(isEmpty) {
    const target = document.getElementById('car-list') || document.getElementById('car-listings');
    if (!target) return;
    if (isEmpty) {
        target.innerHTML = '<div class="alert alert-warning">No cars available.</div>';
    }
}

function loadCarDetails(carId) {
    const carDetails = document.getElementById('car-details');
    const driverDetails = document.getElementById('driver-details');
    const bookingSection = document.getElementById('booking-section');
    if (!carDetails) return;
    fetch(`/api/cars/cars/${carId}/`)
        .then(r => r.json())
        .then(car => {
            const imageUrl = car.car_image || '/media/cars/download.jpg';
            const isBoth = String(car.car_type_name || '').toLowerCase() === 'both';
            const acPrice = car.ac_price_per_km;
            const nonAcPrice = car.non_ac_price_per_km;
            const defaultPrice = car.price_per_km;
            const priceForCart = isBoth ? (acPrice || 0) : (defaultPrice || 0);
            const priceSection = isBoth
                ? `${acPrice ? `<span class="badge bg-info me-2">AC: ₹${acPrice}/km</span>` : ''}${nonAcPrice ? `<span class="badge bg-secondary">Non-AC: ₹${nonAcPrice}/km</span>` : ''}`
                : `${defaultPrice ? `<span class="badge bg-primary">₹${defaultPrice}/km</span>` : ''}`;
            const availabilityBadge = car.is_available ? '<span class="badge bg-success">Available</span>' : '<span class="badge bg-danger">Not Available</span>';
            const headerHtml = `
                <div class="d-flex align-items-center mb-3">
                    <img src="${imageUrl}" alt="${car.name}" style="width: 160px; height: 120px; object-fit: cover; border-radius: 8px;" class="me-3"/>
                    <div>
                        <h3 class="mb-1">${car.name}</h3>
                        <div class="mb-2">
                            ${car.car_model_name ? `<span class="badge bg-dark me-2">${car.car_model_name}</span>` : ''}
                            ${car.car_type_name ? `<span class="badge bg-warning text-dark">${car.car_type_name}</span>` : ''}
                        </div>
                        <div class="mb-2">${priceSection}</div>
                        ${availabilityBadge}
                    </div>
                </div>
            `;
            const detailsHtml = `
                <div class="row">
                    <div class="col-12">
                        ${headerHtml}
                        <div class="d-grid gap-2 mt-3">
                            <button class="btn btn-outline-success" ${car.is_available ? '' : 'disabled'} onclick="addToCart(${car.id}, '${String(car.name).replace(/'/g, "\'")}', '${car.car_type_name}', '${imageUrl}', ${priceForCart})">
                                <i class="bi bi-cart-plus me-1"></i>Add to Cart
                            </button>
                        </div>
                    </div>
                </div>
            `;
            carDetails.innerHTML = detailsHtml;
            if (bookingSection) {
                bookingSection.style.display = car.is_available ? 'block' : 'none';
                bookingSection.querySelector('.card-body').innerHTML = `
                    <a href="/booking/" class="btn btn-success w-100"><i class="bi bi-calendar-check me-1"></i>Proceed to Booking</a>
                `;
            }
            if (driverDetails && car.driver) {
                fetch(`/api/cars/drivers/${car.driver}/`)
                    .then(d => d.json())
                    .then(driver => {
                        const photo = driver.profile_photo || '';
                        driverDetails.innerHTML = `
                            <div class="d-flex align-items-center">
                                ${photo ? `<img src="${photo}" alt="${driver.name}" style="width: 64px; height: 64px; object-fit: cover; border-radius: 50%;" class="me-3"/>` : ''}
                                <div>
                                    <h6 class="mb-1">${driver.name}</h6>
                                    <div class="text-muted">${driver.phone || ''}</div>
                                    <div class="text-muted">${driver.license_number || ''}</div>
                                    <div class="text-muted">${typeof driver.experience === 'number' ? driver.experience + ' years experience' : ''}</div>
                                </div>
                            </div>
                        `;
                    })
                    .catch(() => {
                        driverDetails.innerHTML = '<div class="text-muted">Driver details not available</div>';
                    });
            }
        })
        .catch(() => {
            carDetails.innerHTML = '<div class="alert alert-danger">Failed to load car details.</div>';
        });
}

function loadCars() {
    const target = document.getElementById('car-list');
    if (!target) return;
    fetch('/api/cars/cars/')
        .then(r => r.json())
        .then(data => {
            // Handle paginated API response
            const items = data.results || (Array.isArray(data) ? data : []);
            displayCars(items.slice(0, 6));
        })
        .catch(() => {
            if (target) target.innerHTML = '<div class="alert alert-danger">Failed to load cars.</div>';
        });
}

function loadAllCars() {
    const target = document.getElementById('car-listings') || document.getElementById('car-list');
    if (!target) return;
    
    // Check if we're on the grouped cars page (has data attribute)
    const isGroupedPage = document.querySelector('[data-grouped-cars-page="true"]');
    if (isGroupedPage) {
        // Don't override the server-side rendered grouped content
        return;
    }
    
    // Check if we're on a model-specific page (URL contains /cars/category/[number]/)
    const isModelSpecificPage = window.location.pathname.match(/\/cars\/category\/\d+\//);
    if (isModelSpecificPage) {
        // Don't override the server-side rendered model-specific content
        return;
    }
    
    fetch('/api/cars/cars/')
        .then(r => r.json())
        .then(data => {
            // Handle paginated API response
            const items = data.results || (Array.isArray(data) ? data : []);
            displayCars(items);
        })
        .catch(() => {
            if (target) target.innerHTML = '<div class="alert alert-danger">Failed to load cars.</div>';
        });
}

function setupFilters() {}

function handleSearch(e) {
    const q = (e.target.value || '').toLowerCase();
    const cards = document.querySelectorAll('#car-list .card, #car-listings .card');
    cards.forEach(card => {
        const title = card.querySelector('.card-title');
        const text = title ? title.textContent.toLowerCase() : '';
        card.parentElement.style.display = text.includes(q) ? 'block' : 'none';
    });
}

function handleSort(e) {
    const v = e.target.value || '';
    const list = document.getElementById('car-listings') || document.getElementById('car-list');
    if (!list) return;
    const items = Array.from(list.children);
    if (v === 'price_asc' || v === 'price_desc') {
        items.sort((a, b) => {
            const ap = Number((a.querySelector('.car-price') || {textContent:''}).textContent.replace(/[^\d.]/g, '')) || 0;
            const bp = Number((b.querySelector('.car-price') || {textContent:''}).textContent.replace(/[^\d.]/g, '')) || 0;
            return v === 'price_asc' ? ap - bp : bp - ap;
        });
        items.forEach(it => list.appendChild(it));
    }
}

function loadMyBookings() {
    const container = document.getElementById('bookings-list');
    const loading = document.getElementById('loading');
    const empty = document.getElementById('no-bookings');
    if (!container) return;
    if (loading) loading.style.display = 'block';
    fetch('/api/booking/booking/my/')
        .then(r => {
            if (r.status === 401) return {unauth: true};
            return r.json();
        })
        .then(data => {
            if (loading) loading.style.display = 'none';
            if (data && data.unauth) {
                container.innerHTML = '<div class="alert alert-warning">Please log in to view your bookings.</div>';
                return;
            }
            const items = Array.isArray(data) ? data : [];
            if (!items.length) {
                if (empty) empty.style.display = 'block';
                return;
            }
            let html = '';
            items.forEach(b => {
                const car = b.car_details || {};
                const img = car.car_image || '/media/cars/download.jpg';
                const title = car.name || 'Car';
                html += `
                    <div class="card border-0 shadow-sm mb-3">
                        <div class="row g-0">
                            <div class="col-md-3">
                                <img src="${img}" alt="${title}" class="img-fluid" style="height:100%;object-fit:cover; border-top-left-radius:16px; border-bottom-left-radius:16px;"/>
                            </div>
                            <div class="col-md-9">
                                <div class="card-body">
                                    <h5 class="card-title mb-1">${title}</h5>
                                    <div class="text-muted mb-2">Pickup: ${b.pickup_location || ''} | Drop: ${b.drop_location || ''}</div>
                                    <div class="mb-2"><span class="badge badge-active">${b.booking_status || 'active'}</span></div>
                                    <div class="fw-semibold">Total: ₹${b.total_price || '0.00'}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            });
            container.innerHTML = html;
        })
        .catch(() => {
            if (loading) loading.style.display = 'none';
            container.innerHTML = '<div class="alert alert-danger">Failed to load bookings.</div>';
        });
}