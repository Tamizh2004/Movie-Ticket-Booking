# Movie-Ticket-Booking  -  Django Project

A simple movie ticket booking web application built with Django.

## Features

- List available movies
- Book tickets
- Generate PDF ticket (sample included)
- Admin panel for managing shows

## How to Run

2. Set up environment and install dependencies:
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   pip install -r requirements.txt

3. Run migrations:
   python manage.py migrate

4. Start the server:
   python manage.py runserver

5. Visit `http://127.0.0.1:8000/`

## Admin Access
   python manage.py createsuperuser

Use Django admin to manage movies and bookings.



##  Screenshots

###  Home Page
- [Home Page](screenshots/homepage.jpg)

###  Booking Page
- [Booking Page](screenshots/booking_page.jpg)

###  Admin Panel
- [Admin Panel](screenshots/admin_panel.jpg)

###  Seat Selection
- [Seat Selection](screenshots/seat_selection.jpg)

###  Booking Confirmation
- [Booking Confirmation](screenshots/booking_confirmation.jpg)

###  Payment Page
- [Payment Page](screenshots/payment_page.jpg)


