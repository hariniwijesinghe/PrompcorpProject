# promoCorp

This is a web-based facility management system developed for PrompCorp, a leading Australian Facilities Services business. The system aims to streamline asset and facility management processes, enhance efficiency, customization, and cost-effectiveness, and provide better control over operations across Australia and New Zealand.

## Features

- **User Management:** Allows administrators to manage user accounts, including creation, editing, and deletion.
- **Client Management:** Provides functionality for managing client groups, accounts, and contracts.
- **Department Management:** Enables management of departments, employees, and timesheets.
- **Supplier Management:** Allows management of suppliers, invoices, and material inventory.
- **Material Management:** Facilitates management of materials, store branches, and material invoices.

## Installation

1. Clone the repository to your local machine.
2. Install Python and Django if not already installed.
3. Create a virtual environment and activate it.
4. Install dependencies using `pip install -r requirements.txt`.
5. Set up the database by running `python manage.py migrate`.
6. Create a superuser account using `python manage.py createsuperuser`.
7. Start the development server with `python manage.py runserver`.

## Usage

1. Access the admin interface by navigating to [http://localhost:8000/admin](http://localhost:8000/admin) and log in with your superuser credentials.
2. Use the various modules in the system to manage users, clients, departments, suppliers, materials, and more.
3. Customize the system according to your specific requirements by modifying the Django models, views, and templates.
