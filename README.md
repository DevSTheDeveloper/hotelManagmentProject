# Hotel Management System

## Overview
[Hotel Managment System Documentation .pdf](https://github.com/user-attachments/files/17366841/Hotel.Managment.System.Documentation.pdf)

The Hotel Management System is a web-based application that allows hotel staff to manage room reservations, check-in/check-out guests, and perform various administrative tasks. This system provides an efficient way to streamline hotel operations and improve the guest experience.

<img width="1800" alt="Screenshot 2023-11-23 at 11 30 03" src="https://github.com/DevSTheDeveloper/hotelManagmentProject/assets/83958063/d869ce65-d5e8-4a2f-9374-dff5266eb918">

<img width="1800" alt="Screenshot 2023-11-23 at 11 29 24" src="https://github.com/DevSTheDeveloper/hotelManagmentProject/assets/83958063/bfb14360-49ee-4f1b-82a2-a2847538a7cd">

<img width="1800" alt="Screenshot 2023-11-23 at 11 28 49" src="https://github.com/DevSTheDeveloper/hotelManagmentProject/assets/83958063/0b5de63a-dd0c-4167-b394-22d8c951a25d">

<img width="1800" alt="Screenshot 2023-11-23 at 11 29 48" src="https://github.com/DevSTheDeveloper/hotelManagmentProject/assets/83958063/e06ffaae-5e09-4acd-aadc-c2c81f0a6c7f">




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

