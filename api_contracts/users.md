# 👤 Users API Contract

## Overview

The Users API manages both admin and client accounts. Each user has authentication credentials, contact information, and a defined role (`admin` or `client`).

### Base URL
```
/api/users
```

### Authentication
All endpoints require authentication via JWT Bearer token unless otherwise specified.

#### Request Headers
```
Authorization: Bearer <jwt_token>
```

---

## 📘 Endpoints

### 1. Create User

**`POST /api/users/create`**

#### Description
Create a new user (admin or client).

#### Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

#### Request Body (JSON)
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securePassword123",
  "role": "client",
  "phone_number": "+21612345678"
}
```

#### Constraints
* `role` must be one of: `"admin"`, `"client"`.
* `username`, `email`, and `phone_number` (if provided) must be unique.

#### Responses

| Status | Description | Body |
|--------|-------------|------|
| `201 Created` | User successfully created | `{ "id": 1, "username": "john_doe", "email": "john@example.com", "role": "client", "created_at": "...", "updated_at": "..." }` |
| `400 Bad Request` | Validation or constraint error | `{ "error": "Email already exists" }` |
| `401 Unauthorized` | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| `403 Forbidden` | Insufficient permissions | `{ "error": "Insufficient permissions" }` |

---

### 2. Create Admin

**`POST /api/users/create-admin`**

#### Description
Create a new admin user. This endpoint may require super-admin privileges or special authorization.

#### Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

#### Request Body (JSON)
```json
{
  "username": "admin_user",
  "email": "admin@example.com",
  "password": "secureAdminPass123",
  "phone_number": "+21612345678"
}
```

#### Constraints
* `username`, `email`, and `phone_number` (if provided) must be unique.
* This endpoint automatically sets `role` to `"admin"`.

#### Responses

| Status | Description | Body |
|--------|-------------|------|
| `201 Created` | Admin successfully created | `{ "id": 2, "username": "admin_user", "email": "admin@example.com", "role": "admin", "created_at": "...", "updated_at": "..." }` |
| `400 Bad Request` | Validation or constraint error | `{ "error": "Email already exists" }` |
| `401 Unauthorized` | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| `403 Forbidden` | Insufficient permissions | `{ "error": "Unauthorized to create admin users" }` |

---

### 3. Get All Users

**`GET /api/users`**

#### Description
Retrieve a list of all users (admin-only access).

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Query Parameters (optional)

| Name | Type | Description |
|------|------|-------------|
| `role` | string | Filter users by role (`admin` or `client`) |
| `search` | string | Search by username or email |

#### Example
```
GET /api/users?role=client
```

#### Response
```json
[
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "client",
    "phone_number": "+21612345678",
    "created_at": "2025-11-04T10:00:00Z",
    "updated_at": "2025-11-04T10:00:00Z"
  }
]
```

#### Response Codes

| Status | Description | Body |
|--------|-------------|------|
| `200 OK` | Users retrieved successfully | Array of user objects |
| `401 Unauthorized` | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| `403 Forbidden` | Insufficient permissions | `{ "error": "Admin access required" }` |

---

### 4. Get User by ID

**`GET /api/users/{id}`**

#### Description
Fetch details of a specific user.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Response

| Status | Description | Body |
|--------|-------------|------|
| `200 OK` | User found | `{ "id": 1, "username": "john_doe", "email": "john@example.com", "role": "client", "phone_number": "+21612345678", "created_at": "...", "updated_at": "..." }` |
| `401 Unauthorized` | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| `403 Forbidden` | Insufficient permissions | `{ "error": "Insufficient permissions" }` |
| `404 Not Found` | User does not exist | `{ "error": "User not found" }` |

---

### 5. Get User by Email

**`GET /api/users/email/{email}`**

#### Description
Fetch details of a specific user by their email address.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Example
```
GET /api/users/email/john@example.com
```

#### Response

| Status | Description | Body |
|--------|-------------|------|
| `200 OK` | User found | `{ "id": 1, "username": "john_doe", "email": "john@example.com", "role": "client", "phone_number": "+21612345678", "created_at": "...", "updated_at": "..." }` |
| `400 Bad Request` | Invalid email format | `{ "error": "Invalid email format" }` |
| `401 Unauthorized` | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| `403 Forbidden` | Insufficient permissions | `{ "error": "Insufficient permissions" }` |
| `404 Not Found` | User does not exist | `{ "error": "User not found" }` |

---

### 6. Update User

**`PUT /api/users/{id}`**

#### Description
Update user information. Password changes should be handled via a separate route (e.g. `/api/users/{id}/password`).

#### Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

#### Request Body (JSON)
```json
{
  "username": "john_updated",
  "email": "john_new@example.com",
  "phone_number": "+21699887766",
  "role": "client"
}
```

#### Response

| Status | Description | Body |
|--------|-------------|------|
| `200 OK` | User updated successfully | `{ "id": 1, "username": "john_updated", "email": "john_new@example.com", "role": "client", "updated_at": "2025-11-04T11:00:00Z" }` |
| `400 Bad Request` | Invalid data or duplicate field | `{ "error": "Email already exists" }` |
| `401 Unauthorized` | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| `403 Forbidden` | Insufficient permissions | `{ "error": "Insufficient permissions" }` |
| `404 Not Found` | User not found | `{ "error": "User not found" }` |

---

### 7. Delete User

**`DELETE /api/users/{id}`**

#### Description
Delete a user account. Cascade Behavior: Deleting a user will also delete their associated factory and related data.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Response

| Status | Description | Body |
|--------|-------------|------|
| `204 No Content` | User deleted successfully | — |
| `401 Unauthorized` | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| `403 Forbidden` | Insufficient permissions | `{ "error": "Insufficient permissions" }` |
| `404 Not Found` | User not found | `{ "error": "User not found" }` |

---

### 8. Delete Admin

**`DELETE /api/users/admin/{id}`**

#### Description
Delete an admin account. This endpoint requires super-admin privileges or special authorization. Cascade Behavior: Deleting an admin will also delete their associated data.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Response

| Status | Description | Body |
|--------|-------------|------|
| `204 No Content` | Admin deleted successfully | — |
| `400 Bad Request` | Cannot delete last admin or self | `{ "error": "Cannot delete the last admin account" }` or `{ "error": "Cannot delete your own admin account" }` |
| `401 Unauthorized` | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| `403 Forbidden` | Insufficient permissions | `{ "error": "Unauthorized to delete admin users" }` |
| `404 Not Found` | Admin not found | `{ "error": "Admin not found" }` |

---

### 9. Update Password

**`PATCH /api/users/{id}/password`**

#### Description
Change a user's password securely.

#### Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

#### Request Body
```json
{
  "old_password": "oldPass123",
  "new_password": "newPass456"
}
```

#### Response

| Status | Description | Body |
|--------|-------------|------|
| `200 OK` | Password updated | `{ "message": "Password updated successfully" }` |
| `400 Bad Request` | Invalid old password | `{ "error": "Incorrect old password" }` |
| `401 Unauthorized` | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| `403 Forbidden` | Insufficient permissions | `{ "error": "Insufficient permissions" }` |
| `404 Not Found` | User not found | `{ "error": "User not found" }` |