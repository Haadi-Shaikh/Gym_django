# Gym Management System

A simple and clean Gym Management System built with Django, SQLite, Bootstrap, and basic custom CSS.

## Features

- Member registration, login, logout
- Profile page
- Membership plan listing
- Plan selection without payment
- Dashboard with active and expired subscription status
- Django admin for managing plans and subscriptions

## Run the project

```bash
python manage.py runserver
```

Open:

- App: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

## Create an admin user

```bash
python manage.py createsuperuser
```

## Main models

- `MembershipPlan`
- `Subscription`

The project uses SQLite by default, so no extra database setup is needed.
