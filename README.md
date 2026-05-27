# NT Housing Maintenance System

## Project Overview

The NT Housing Maintenance System is a Django web application developed for the HIT237 Building Interactive Software group project.

The project focuses on remote housing maintenance in the Northern Territory. The system allows tenants to submit housing repair requests, view request status, and track maintenance progress. Staff or admin users can manage requests, update repair status, and add maintenance updates.

The application supports role-based workflows where tenants and staff have different permissions.

## Group Information

Unit: HIT237 Building Interactive Software  
Project Theme: Remote Housing Crisis NT  
Group: Group 1  

## Repository

https://github.com/ccordoba24/Group1_HIT237

## Main Features

- User registration
- User login and logout
- Role-based request access
- Repair request creation
- Repair request listing
- Repair request detail view
- Repair request editing
- Status tracking
- Maintenance update workflow
- Dashboard metrics
- Admin interface
- FAQ page
- Service layer for business logic
- Custom permission service
- Custom exceptions
- Custom QuerySet manager
- QuerySet annotations and aggregations
- Test suite covering models, services, views, permissions, and QuerySets

## User Roles and Permissions

### Normal User or Tenant

A normal user can:

- Register and log in
- Create repair requests
- View requests they created
- View requests linked to their tenant profile
- View the status of their repair requests
- Edit basic request details

A normal user cannot:

- Edit the official repair status
- View unrelated users' requests
- Add maintenance updates
- Access admin-only workflows

### Staff or Admin User

A staff or admin user can:

- View all repair requests
- Edit repair request status
- Add maintenance updates
- Access broader management features
- Use the Django admin panel

## Demo Login Credentials

Use these accounts to test the application after running the seed data command.

### Admin Account

Username: admin  
Password: Admin12345

### Normal User Account

Username: testuser  
Password: pralin206407

Important: if login does not work, run the seed data command again. The seed command resets the demo account passwords.

```bash
python manage.py seed_data
```

Then try logging in again with the credentials above.

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/ccordoba24/Group1_HIT237.git
```

### 2. Move into the project folder

```bash
cd Group1_HIT237
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

For Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```bash
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Move into the Django project folder

```bash
cd proj_1
```

### 7. Apply migrations

```bash
python manage.py migrate
```

### 8. Load demo data

```bash
python manage.py seed_data
```

This creates or resets the demo accounts and sample repair request data.

### 9. Run the server

```bash
python manage.py runserver
```

### 10. Open the application

Home page:

```text
http://127.0.0.1:8000/
```

Login page:

```text
http://127.0.0.1:8000/login/
```

## Useful Application Links

After running the server, use these links.

Home:

```text
http://127.0.0.1:8000/
```

Login:

```text
http://127.0.0.1:8000/login/
```

Register:

```text
http://127.0.0.1:8000/register/
```

Dashboard:

```text
http://127.0.0.1:8000/dashboard/
```

Repair Requests:

```text
http://127.0.0.1:8000/requests/
```

Create Repair Request:

```text
http://127.0.0.1:8000/requests/new/
```

Maintenance History:

```text
http://127.0.0.1:8000/history/
```

FAQ:

```text
http://127.0.0.1:8000/faq/
```

About:

```text
http://127.0.0.1:8000/about/
```

Django Admin:

```text
http://127.0.0.1:8000/admin/
```

Admin login:

Username: admin  
Password: Admin12345

## How to Test the Main Workflow

### Admin Workflow

1. Open:

```text
http://127.0.0.1:8000/login/
```

2. Login as admin:

Username: admin  
Password: Admin12345

3. Open the dashboard:

```text
http://127.0.0.1:8000/dashboard/
```

4. Open the requests page:

```text
http://127.0.0.1:8000/requests/
```

5. Click a repair request.

Admin should be able to:

- View request details
- See request status
- Edit request status
- Add maintenance updates

### Normal User Workflow

1. Logout.

2. Login as normal user:

Username: testuser  
Password: pralin206407

3. Open:

```text
http://127.0.0.1:8000/dashboard/
```

4. Open:

```text
http://127.0.0.1:8000/requests/
```

Normal user should be able to:

- View only their created or tenant-linked requests
- See the request status
- Edit basic request details

Normal user should not be able to:

- Edit the status field
- Add maintenance updates
- View unrelated users' requests

## Running Tests

Run tests from inside the Django project folder:

```bash
cd proj_1
python manage.py test housing
```

Expected result:

```text
Found 23 test(s).
OK
```

The test suite covers:

- Model behaviour
- Custom QuerySet methods
- QuerySet annotations
- Service layer logic
- Custom permission checks
- Login-required views
- Dashboard access
- Role-based request access
- Status editing restrictions
- Maintenance update restrictions

## If Login Does Not Work

If login fails for the demo accounts, reset the demo data.

From inside:

```text
Group1_HIT237/proj_1
```

Run:

```bash
python manage.py seed_data
```

Then run the server again:

```bash
python manage.py runserver
```

Try logging in again.

Admin:

Username: admin  
Password: Admin12345

Normal user:

Username: testuser  
Password: pralin206407

The seed data command resets the demo account passwords.

## If There Are Migration Warnings

If the server says there are unapplied migrations, stop the server and run:

```bash
python manage.py migrate
```

Then run:

```bash
python manage.py seed_data
python manage.py runserver
```

## Important Folder Note

The repository root is:

```text
Group1_HIT237
```

The Django project folder is:

```text
Group1_HIT237/proj_1
```

Run Django commands from inside:

```text
Group1_HIT237/proj_1
```

Run Git commands from the repository root:

```text
Group1_HIT237
```

## Development Architecture

### Models

The application uses Django models to represent:

- Communities
- Dwellings
- Tenants
- Repair request categories
- Repair requests
- Maintenance updates

Repair requests are linked to tenants, dwellings, categories, and the user who created the request.

### Custom QuerySet Manager

The repair request model uses a custom QuerySet manager to support reusable query logic such as:

- Open requests
- Completed requests
- Pending requests
- In-progress requests
- User-specific requests
- Annotated update counts

This supports cleaner views and stronger object-oriented decomposition.

### Service Layer

Business logic is separated from views using a service layer.

The service layer handles:

- Repair request creation
- Repair request updates
- Permission checks
- Validation
- Transaction handling

This keeps views focused on HTTP request and response handling.

### Permission Service

The permission service manages authorization decisions.

It checks whether:

- A user is staff or admin
- A user can update a repair request
- A user can add maintenance updates

This avoids duplicating permission logic across multiple views.

### Exception Handling

The application includes custom exceptions such as:

- InvalidRepairRequestError
- UnauthorizedRepairActionError

These exceptions make business rule failures clearer and easier to test.

### Authentication and Authorization

The application uses Django authentication for login, logout, registration, and protected views.

Role-based access is applied so that:

- Staff and admin users can manage all requests
- Normal users can only access requests they created or requests linked to their tenant profile
- Normal users can view status but cannot edit status
- Only staff or admin users can add maintenance updates

## Main Commands

From the repository root:

```bash
cd proj_1
python manage.py migrate
python manage.py seed_data
python manage.py test housing
python manage.py runserver
```

## Troubleshooting

### Problem: manage.py not found

You are probably in the repository root instead of the Django project folder.

Fix:

```bash
cd proj_1
python manage.py runserver
```

### Problem: Login does not work

Run:

```bash
python manage.py seed_data
```

Then try:

Username: admin  
Password: Admin12345

### Problem: Database migration warning

Run:

```bash
python manage.py migrate
```

### Problem: Page does not open

Make sure the server is running:

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

### Problem: Tests fail after database changes

Run:

```bash
python manage.py migrate
python manage.py test housing
```

## Submission Notes

Before submission, confirm:

```bash
python manage.py test housing
```

passes successfully.

Current expected test result:

```text
Found 23 test(s).
OK
```

Also confirm that GitHub is clean and pushed:

```bash
git status
```

Expected:

```text
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

## Technologies Used

- Python
- Django
- SQLite
- HTML templates
- Django authentication
- Django class-based views
- Django ORM
- Custom QuerySet manager
- Service layer pattern
- Git and GitHub

## Project Status

The application is runnable and includes authenticated workflows, role-based permissions, service-layer logic, and a test suite. The current development version is ready for final documentation review, ADR updates, and group submission checks.