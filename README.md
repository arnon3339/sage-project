
# Sage Project - FavLinks Web Application (Backend Only)

## Project Overview

**Sage Project** is a backend-only web application named **FavLinks**. This application allows users to manage their favorite URLs, categories, and tags. The project is built using the Django web framework and follows secure practices for user authentication. The application is designed to be user-friendly and efficient in managing and categorizing favorite URLs.

### Objective

Develop a user-friendly web application that enables users to:

- Manage their favorited URLs.
- Organize URLs by categories and tags.
- Perform CRUD operations via RESTful API endpoints.

### Key Features

1. **Django Framework**: Leveraging Django to build a scalable and maintainable project structure.
2. **Database Management**: Uses a database system of your choice with an optimized schema design.
3. **User Authentication**: Includes secure user registration, login, and password reset functionalities.
4. **RESTful API**: Provides API endpoints for CRUD operations on favorited URLs, categories, and tags.

## Installation

### Prerequisites

- Python 3.12.3
- Django
- Other dependencies listed in `requirements.txt`

### Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd sage_project
   ```

2. Set up the virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts activate`
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the environment variables by creating a `.env` file in the root directory. The `.env` file should contain necessary configurations such as database settings and secret keys.

   **Important:** Set the `DJANGO_SECRET_KEY` environment variable in your system to secure JWT token authentication. This key is used as the secret key for generating and verifying JWT tokens.

   Example:
   ```bash
   export DJANGO_SECRET_KEY='your_secret_key_here'
   ```

5. Apply migrations:
   ```bash
   python manage.py migrate
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

After starting the server, you can access the API endpoints through tools like Postman or cURL. The API provides the following functionality:

- **User Authentication**: Register, login, and reset passwords.
- **Manage URLs**: Add, update, delete, and view favorited URLs.
- **Categories and Tags**: Organize URLs using categories and tags.

## Contributing

If you'd like to contribute to this project, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

This project is licensed under the MIT License.