# Vendor Management System with Performance Metrics

This is a Vendor Management System developed using Django and Django REST Framework. It provides functionality to manage vendor profiles, track purchase orders, and calculate vendor performance metrics.

## Prerequisites

- Python 
- Django 
- Django REST Framework
- Django JWT

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/prat8897/vendor_management.git
   cd vendor-management-system
   ```

2. Create and activate a virtual environment (optional but recommended):

    ```
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Apply the database migrations:
    ```
    python manage.py migrate
    ```

5. Create a superuser account:
    ```
    python manage.py createsuperuser
    ```

## Running the Development Server

1. Start the development server:
    ```
    python manage.py runserver
    ```

2. Open your web browser and navigate to http://localhost:8000/api/ to access the API endpoints.

## API Endpoints

The following API endpoints are available:

POST /api/vendors/: Create a new vendor.
GET /api/vendors/: List all vendors.
GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.
PUT /api/vendors/{vendor_id}/: Update a vendor's details.
DELETE /api/vendors/{vendor_id}/: Delete a vendor.
POST /api/purchase_orders/: Create a purchase order.
GET /api/purchase_orders/: List all purchase orders with an option to filter by vendor.
GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
PUT /api/purchase_orders/{po_id}/: Update a purchase order.
DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.
GET /api/vendors/{vendor_id}/performance/: Retrieve a vendor's performance metrics.
POST /api/purchase_orders/{po_id}/acknowledge/: Acknowledge a purchase order.

## Authentication
The API endpoints are secured using token-based authentication. To obtain an access token, send a POST request to /api/token/ with valid user credentials. Include the access token in the Authorization header of subsequent requests.
