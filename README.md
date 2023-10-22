# Hotel Management System

## Overview

The Hotel Management System is a web-based application that allows hotel staff to manage room reservations, check-in/check-out guests, and perform various administrative tasks. This system provides an efficient way to streamline hotel operations and improve the guest experience.

## Features

- **Room Reservations:** Guests can reserve rooms by selecting check-in and check-out dates, choosing room types, and providing their personal information.

- **Guest Check-In/Check-Out:** Hotel staff can check-in guests upon arrival and check them out upon departure.

- **Admin Functions:** Administrators have access to additional features, including marking rooms as "out of order," changing room types, and creating new rooms.

- **Reservation Payment:** Guests can choose their preferred payment method, either credit card or cash.

## Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python (3.6 or higher)
- Django
- Django REST framework
- PostgreSQL (or other supported databases)
- Git (for version control)


## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/hotel-management.git
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv hotel-env
    source hotel-env/bin/activate  # On Windows, use hotel-env\Scripts\activate
    ```

3. **Install project dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a superuser account:**

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

7. **Access the application** in your web browser at [([http://localhost:8000](http://127.0.0.1:8000/homepage/))].

