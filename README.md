# scilems-backend

Welcome to the **scilems-backend** repository! This project serves as the backend for my final project, providing essential user authentication functionalities.

## User Authentication API

This API allows users to register, log in, and access protected routes. Below are the details for each endpoint.

### 1. User Registration

- **Method**: `POST`
- **Endpoint**: `/api/auth/register/`
- **Description**: This endpoint allows new users to create an account by providing a username, email, and password.

- **Request Body** (JSON):

  ```json
  {
    "username": "john",
    "email": "john@example.com",
    "password": "TestPass123",
    "password2": "TestPass123"
  }
  ```

- **Response**:
  - **Success**: Returns a success message and user details.
  - **Error**: Returns validation errors if the input is invalid.

### 2. User Login

- **Method**: `POST`
- **Endpoint**: `/api/auth/login/`
- **Description**: This endpoint allows users to log in by providing their username and password.

- **Request Body** (JSON):

  ```json
  {
    "username": "john",
    "password": "TestPass123"
  }
  ```

- **Response**:
  - **Success**: Returns an access token and user details.
  - **Error**: Returns an error message if the credentials are incorrect.

### 3. Access Protected Route

- **Method**: `GET`
- **Endpoint**: `/api/auth/protected/`
- **Description**: This endpoint is accessible only to authenticated users. It requires a valid Bearer token for access.

- **Authorization**:

  - **Type**: Bearer Token
  - **Token**: Include the access token received from a successful login in the Authorization header:
    ```
    Authorization: Bearer <access_token>
    ```

- **Response**:
  - **Success**: Returns protected resource data.
  - **Error**: Returns an error message if the token is missing or invalid.

## Getting Started

To get started with the scilems-backend, clone the repository and follow the setup instructions in the [Installation Guide](#).

## Contributing

Contributions are welcome! Please read the [Contributing Guidelines](#) for more information on how to contribute to this project.

## License

This project is licensed under the [MIT License](#).

---

Feel free to reach out if you have any questions or need further assistance!
