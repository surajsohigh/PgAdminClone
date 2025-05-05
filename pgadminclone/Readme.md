

# Django SQL Explorer API

A lightweight Django-based API that allows users to:

* View all database tables
* Inspect table data and schema
* Execute raw SQL queries (⚠️ use with caution)


## PgAdmin Endpoints

### `GET /`

Returns a simple welcome message.

### `GET /list_tables/`

Lists all tables in the `public` schema.

### `GET /get_table_data/<table_name>/`

Returns the first 100 rows of the specified table.

### `GET /get_table_columns/<table_name>/`

Returns column names and data types for the specified table.

### `POST /execute_query/`

Executes a raw SQL query. Expects a JSON body:

```json
{
  "sql": "SELECT * FROM your_table"
}
```


## 🛠️ Setup Instructions

1. Clone the repo:

   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
   ```

2. **Set up a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure your database in `settings.py`.

5. Run migrations:

   ```bash
   python manage.py migrate
   ```

6. Run the development server:

   ```bash
   python manage.py runserver
   ```

## 🧪 Example Curl Requests

* List tables:

  ```bash
  curl http://localhost:8000/list_tables/
  ```

* Get table data:

  ```bash
  curl http://localhost:8000/get_table_data/your_table/
  ```

* Execute SQL:

  ```bash
  curl -X POST -H "Content-Type: application/json" \
       -d '{"sql": "SELECT * FROM your_table"}' \
       http://localhost:8000/execute_query/
  ```

## 🔐 Authentication Endpoints

### `POST /login/` – User Login

Authenticates a user and returns access and refresh tokens.

**Request:**

```bash
curl -X POST http://localhost:8000/login/ \
     -H "Content-Type: application/json" \
     -d '{
           "email": "user@example.com",
           "password": "yourpassword"
         }'
```

**Response:**

```json
{
  "message": "Login Sucessfull",
  "token": {
    "refresh": "your-refresh-token",
    "access": "your-access-token"
  }
}
```

---

### `POST /register/` – User Registration

Creates a new user account and returns JWT tokens.

**Request:**

```bash
curl -X POST http://localhost:8000/register/ \
     -H "Content-Type: application/json" \
     -d '{
           "email": "newuser@example.com",
           "password": "newpassword",
           "confirm_password": "newpassword",
           "first_name": "John",
           "last_name": "Doe"
         }'
```

**Response:**

```json
{
  "message": "Created Sucessfully",
  "Token": {
    "refresh": "your-refresh-token",
    "access": "your-access-token"
  }
}
```

---

### `GET /profile/` – Get User Profile

Fetches the authenticated user's profile.

**Request:**

```bash
curl -X GET http://localhost:8000/profile/ \
     -H "Authorization: Bearer your-access-token"
```

**Response:**

```json
{
  "user data": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "message": "User Data Fetched Sucessfully"
}
```

---

### `POST /logout/` – User Logout

Blacklists the refresh token (requires Django REST Framework SimpleJWT with blacklisting enabled).

**Request:**

```bash
curl -X POST http://localhost:8000/logout/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer your-access-token" \
     -d '{
           "refresh": "your-refresh-token"
         }'
```

**Response:**

```json
{
  "success": "Logged out successfully."
}
```

---

Let me know if you want help documenting this using Swagger or DRF’s built-in schema generator.

