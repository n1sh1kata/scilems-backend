# scilems-backend

Welcome to the **scilems-backend** repository! This project serves as the backend for my final project, providing essential user authentication and resource management functionalities.

## API Endpoints

Below is the documentation for the available API endpoints.

---

### 1. User Authentication

#### a. User Registration

- **Method**: `POST`
- **Endpoint**: `/api/auth/register/`
- **Description**: Allows new users to create an account.

- **Request Body**:

  ```json
  {
    "username": "john",
    "email": "john@example.com",
    "password": "TestPass123",
    "password2": "TestPass123"
  }
  ```

- **Response**:
  - **Success**:
    ```json
    {
      "message": "User registered successfully.",
      "user": {
        "username": "john",
        "email": "john@example.com"
      }
    }
    ```
  - **Error**:
    ```json
    {
      "password": ["Passwords do not match."]
    }
    ```

#### b. User Login

- **Method**: `POST`
- **Endpoint**: `/api/auth/login/`
- **Description**: Allows users to log in and retrieve access and refresh tokens.

- **Request Body**:

  ```json
  {
    "username": "john",
    "password": "TestPass123"
  }
  ```

- **Response**:
  - **Success**:
    ```json
    {
      "access": "<access_token>",
      "refresh": "<refresh_token>"
    }
    ```
  - **Error**:
    ```json
    {
      "detail": "No active account found with the given credentials."
    }
    ```

#### c. Token Refresh

- **Method**: `POST`
- **Endpoint**: `/api/auth/token/refresh/`
- **Description**: Refreshes the access token using the refresh token.

- **Request Body**:

  ```json
  {
    "refresh": "<refresh_token>"
  }
  ```

- **Response**:
  - **Success**:
    ```json
    {
      "access": "<new_access_token>"
    }
    ```

#### d. Logout

- **Method**: `POST`
- **Endpoint**: `/api/auth/logout/`
- **Description**: Logs out the user by blacklisting the refresh token.

- **Request Body**:

  ```json
  {
    "refresh": "<refresh_token>"
  }
  ```

- **Response**:
  - **Success**:
    ```json
    {
      "message": "Successfully logged out."
    }
    ```
  - **Error**:
    ```json
    {
      "error": "Refresh token is required."
    }
    ```

#### e. Protected Route

- **Method**: `GET`
- **Endpoint**: `/api/auth/protected/`
- **Description**: Accessible only to authenticated users.

- **Headers**:

  ```
  Authorization: Bearer <access_token>
  ```

- **Response**:
  - **Success**:
    ```json
    {
      "message": "Hello, john!"
    }
    ```
  - **Error**:
    ```json
    {
      "detail": "Authentication credentials were not provided."
    }
    ```

---

### 2. Equipment Management

#### a. List Categories

- **Method**: `GET`
- **Endpoint**: `/api/equipment/categories/`
- **Description**: Retrieves a list of all equipment categories.

- **Headers**:

  ```
  Authorization: Bearer <access_token>
  ```

- **Response**:
  ```json
  [
    {
      "id": 1,
      "categoryname": "Microscopes"
    },
    {
      "id": 2,
      "categoryname": "Chemicals"
    }
  ]
  ```

#### b. Create Equipment

- **Method**: `POST`
- **Endpoint**: `/api/equipment/equipments/`
- **Description**: Allows admin users to create new equipment.

- **Headers**:

  ```
  Authorization: Bearer <access_token>
  ```

- **Request Body**:

  ```json
  {
    "category": 1,
    "eqname": "Microscope X200",
    "stock": 10,
    "description": "High-quality microscope."
  }
  ```

- **Response**:
  - **Success**:
    ```json
    {
      "id": 1,
      "category": 1,
      "eqname": "Microscope X200",
      "stock": 10,
      "description": "High-quality microscope."
    }
    ```
  - **Error**:
    ```json
    {
      "stock": ["Stock cannot be negative."]
    }
    ```

---

### 3. Cart Management

#### a. Add to Cart

- **Method**: `POST`
- **Endpoint**: `/api/cart/`
- **Description**: Adds an item to the user's cart.

- **Headers**:

  ```
  Authorization: Bearer <access_token>
  ```

- **Request Body**:

  ```json
  {
    "equipment": 1,
    "quantity": 2
  }
  ```

- **Response**:
  - **Success**:
    ```json
    {
      "id": 1,
      "user": 1,
      "equipment": 1,
      "quantity": 2
    }
    ```
  - **Error**:
    ```json
    {
      "quantity": ["Only 5 units of 'Microscope X200' are available."]
    }
    ```

#### b. View Cart

- **Method**: `GET`
- **Endpoint**: `/api/cart/`
- **Description**: Retrieves the user's cart items.

- **Headers**:

  ```
  Authorization: Bearer <access_token>
  ```

- **Response**:
  ```json
  [
    {
      "id": 1,
      "user": 1,
      "equipment": 1,
      "quantity": 2
    }
  ]
  ```

---

### 4. Transaction Management

#### a. Create Transaction

- **Method**: `POST`
- **Endpoint**: `/api/transaction/`
- **Description**: Creates a new transaction for the user.

- **Headers**:

  ```
  Authorization: Bearer <access_token>
  ```

- **Request Body**:

  ```json
  {
    "cart_ids": [1, 2],
    "remarks": "Urgent request."
  }
  ```

- **Response**:
  - **Success**:
    ```json
    {
      "id": 1,
      "user": 1,
      "current_status": "applying",
      "remarks": "Urgent request."
    }
    ```
  - **Error**:
    ```json
    {
      "carts": ["You can only include your own cart items in a transaction."]
    }
    ```

---

## Getting Started

To get started with the scilems-backend, clone the repository and follow the setup instructions in the [Installation Guide](#).

## Contributing

Contributions are welcome! Please read the [Contributing Guidelines](#) for more information on how to contribute to this project.

## License

This project is licensed under the [MIT License](#).

---
