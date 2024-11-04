# Employee Management REST API
A Django REST API for managing employees with CRUD operations, JWT-based authentication, pagination, and filtering.

Features
CRUD Operations: Create, retrieve, update, and delete employees.

JWT Authentication: Secure access with token-based authentication.

Filtering and Pagination: Filter by department and role, paginate results.

Setup Instructions

1. Clone the Repository 
git clone https://github.com/adipatil6464/habot_project

cd employee_management_project

3. Set Up Environment 
# Create and activate virtual environment
python -m venv env

# On Windows
.\env\Scripts\activate
# On macOS/Linux
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

3. Run Migrations:
python manage.py migrate

4. Create Superuser:
python manage.py createsuperuser

5. Start the Server:
python manage.py runserver

The API is now available at http://127.0.0.1:8000/.

Endpoints
Authentication

POST /api/token/: Get access and refresh tokens.

POST /api/token/refresh/: Refresh the access token.

Employee Management

POST /api/employees/: Create a new employee.

GET /api/employees/: List all employees, with optional pagination and filtering by department and role.

GET /api/employees/{id}/: Retrieve a specific employee by ID.

PUT /api/employees/{id}/: Update an employee’s details.

DELETE /api/employees/{id}/: Delete an employee by ID.

Authentication
Get a token by making a POST request to /api/token/ with a JSON body containing username and password.

Use the token in the headers for authenticated requests: 
Authorization: Bearer <your_access_token>

Running Tests
Run tests for the employees API with:
 
python manage.py test employees
