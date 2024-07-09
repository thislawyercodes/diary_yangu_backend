# Django Backend for Journal App

This Django backend serves as the API for the Journal App, providing endpoints for user management, journal entry management, data summary, and ensuring security.

## Features
1. **User Management**
   - User registration and authentication using JWT tokens or session-based authentication.
   - Profile management for users.

2. **Journal Entry Management**
   - CRUD operations for journal entries.
   - Categorization of entries.

3. **Data Summary**
   - Endpoints to fetch summary data for given periods, such as aggregated statistics or reports.

4. **Security**
   - Secure all endpoints and allow access only to authenticated users.
   - Use HTTPS for secure communication.
   - Implement authentication mechanisms to protect sensitive operations.

5. **Database**
   - Use a relational database like PostgreSQL or MySQL for data storage and retrieval.
   - Ensure database schema supports journal entries, categories, and user profiles efficiently.

## API Endpoints
Ensure the backend exposes the following endpoints:

- **User Authentication**:
  - `POST /api/auth/register`: Register a new user.
  - `POST /api/auth/login`: Log in and obtain an authentication token.
  - `POST /api/auth/logout`: Log out the user and invalidate the token.
  - `GET /api/auth/user`: Fetch the current user's profile.

- **Journal Entries**:
  - `GET /api/journal/entries/`: Fetch all journal entries.
  - `POST /api/journal/entries/`: Create a new journal entry.
  - `GET /api/journal/entries/:id/`: Retrieve a specific journal entry.
  - `PUT /api/journal/entries/:id/`: Update a journal entry.
  - `DELETE /api/journal/entries/:id/`: Delete a journal entry.

- **Categories**:
  - `GET /api/journal/categories/`: Fetch all categories.
  - `POST /api/journal/categories/`: Create a new category.
  - `GET /api/journal/categories/:id/`: Retrieve a specific category.
  - `PUT /api/journal/categories/:id/`: Update a category.
  - `DELETE /api/journal/categories/:id/`: Delete a category.

- **Data Summary**:
  - `GET /api/journal/summary/`: Retrieve summary data for given periods (e.g., monthly stats).

## Security Considerations
- Implement JWT token-based authentication for securing API endpoints.
- Validate user inputs and handle errors gracefully.
- Use HTTPS for secure data transmission.
- Apply appropriate permissions to restrict access to sensitive endpoints.

## Database Schema
Ensure the database schema supports the following entities:

- **User**:
  - `id`
  - `username`
  - `email`
  - `password`
  - `created_at`
  - `updated_at`

- **Profile**:
  - `id`
  - `user_id` (Foreign Key to User)
  - `full_name`
  - `bio`
  - `avatar_url`
  - `created_at`
  - `updated_at`

- **JournalEntry**:
  - `id`
  - `user_id` (Foreign Key to User)
  - `title`
  - `content`
  - `created_at`
  - `updated_at`

- **Category**:
  - `id`
  - `title`
  - `description`
  - `color`
  - `created_at`
  - `updated_at`

## Installation
* If you wish to run your this backend, first ensure you have python and pip3 globally installed in your computer. 
* After doing this, confirm that you have installed virtualenv globally as well. If not, run this:
    ```bash
        $ pip install virtualenv
    ```
* Then, Git clone this repo to your PC
    ```bash
        $https://github.com/thislawyercodes/diary_yangu_backend/
    ```
* #### Dependencies
    1. Cd into your the cloned repo as such:
        ```bash
            $ cd diary-yangu
    2. Create and fire up your virtual environment:
        ```bash
            $ virtualenv  venv -p python3
            $ source venv/bin/activate
        ```
     3. Create a .env file with the following environment variables
------------------------------------------------------------------
``` bash
` SECRET_KEY=yoursecretkey
DATABASE_NAME=yourdb
DATABASE_USER=yourdbuser
DATABASE_PASSWORD=yourbdpassword
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

    4. Install the dependencies needed to run the app:
        ```bash
            $ pip3 install -r requirements.txt
        ```
    5 . Run Unit Tests
        ----------------------
        ``` shell
           python3 manage.py test

    6. Make those migrations work
        ```bash
            $ python manage.py makemigrations
            $ python manage.py migrate
        ```

* #### Run It
    Fire up the server using this one simple command:
  
    ```bash
        $ python manage.py runserver
   
  




