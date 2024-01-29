# Django Rest Framework Project

This project is a Django Rest Framework (DRF) implementation for handling user authentication, friend requests, and interactions for a social networking app.

## Setup

### Prerequisites

- Python (3.12.1)
- Django (5.0.1)
- Django Rest Framework (3.14.0)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/tejas-21sept/social_network_backend.git
   cd social_network_backend
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py runserver

# Social Networking App Backend with Django REST Framework

**A robust REST API for powering user authentication, friend connections, and social interactions.**

## Features

- **Secure User Authentication:** Token-based authentication with password hashing and optional email verification.
- **Friend Requests and Connections:** Manage friend requests, accept/reject connections, and view a user's friend list.
- **Social Interactions:** Post status updates, view friends' feeds, and interact with posts (like, comment).

## Technologies Used

- Python 3.12.1
- Django 5.0.1
- Django REST Framework 3.14.0
- MySQL (or your preferred database)

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/tejas-21sept/social_network_backend.git
   
2. Create a virtual environment and activate it:

  python -m venv venv
  source venv/bin/activate  # Linux/macOS
  venv\Scripts\activate.bat  # Windows

3. Install dependencies:

  pip install -r requirements.txt

4. Create a .env file:

  > Create a file named .env in the root directory of the project.
  > Copy the contents of the .env-example file into .env.
  > Fill in the appropriate values for your environment variables, such as API keys, database credentials, and any other sensitive information.

5. Apply database migrations
   
  python manage.py makemigrations
  python manage.py migrate

6. Run the development server:

   python manage.py runserver


## Resources

1. Project Link
  **Project Repository:** [Social Network Backend](https://github.com/tejas-21sept/social_network_backend)

2. Postman Collection
   





