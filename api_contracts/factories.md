# 🏭 Factory API Contract

## Overview

The Factory API manages factory entities and their relationships with users. Each client user owns exactly one factory, while admins can view and manage all factories.

### Base URL
```
/api/factories
```

### Authentication
All endpoints require authentication via JWT Bearer token.

#### Request Headers
```
Authorization: Bearer <jwt_token>
```

---

## 📘 Endpoints

### 1. Get All Factories

**`GET /api/factories`**

#### Description
Retrieve a list of all factories (admin-only access).

#### Headers
```
Authorization: Bearer <jwt_token>
```
#### Response
```json
[
  {
    "id": 1,
    "name": "Textile Factory Alpha",
    "location": "Tunis, Tunisia",
    "description": "Main textile production facility",
    "owner_id": 5,
    "created_at": "2025-11-04T10:00:00Z",
    "updated_at": "2025-11-04T10:00:00Z"
  },
  {
    "id": 2,
    "name": "Manufacturing Plant Beta",
    "location": "Sfax, Tunisia",
    "description": "Secondary manufacturing site",
    "owner_id": 8,
    "created_at": "2025-11-03T14:30:00Z",
    "updated_at": "2025-11-03T14:30:00Z"
  }
]
```

#### Response Codes

| Status | Description | Body |
|--------|-------------|------|
| `200 OK` | Factories retrieved successfully | Array of factory objects |
| `401 Unauthorized` | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
---

### 2. Get Factory by ID

**`GET /api/factories/{factory_id}`**

#### Description
Retrieve detailed information about a specific factory by its ID.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Response

| Status | Description | Body |
|--------|-------------|------|
| `200 OK` | Factory found | `{ "id": 1, "name": "Textile Factory Alpha", "location": "Tunis, Tunisia", "description": "Main textile production facility", "user_id": 5, "created_at": "...", "updated_at": "..." }` |
| `401 Unauthorized` | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` 
---

### 4. Create Factory

**`POST /api/factories/create`**

#### Description
Create a new factory (usually when a new client is added or registered).

#### Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

#### Request Body (JSON)
```json
{
  "name": "New Manufacturing Plant",
  "location": "Sousse, Tunisia",
  "description": "Advanced manufacturing facility with automated systems",
  "owner_id": 10
}
```

#### Constraints
* `owner_id` must reference an existing client user.
* Each client can own only one factory.
* `name` is required.

#### Responses

| Status | Description | Body |
|--------|-------------|------|
| `201 Created` | Factory successfully created | `{ "id": 3, "name": "New Manufacturing Plant", "location": "Sousse, Tunisia", "description": "Advanced manufacturing facility with automated systems", "user_id": 10, "created_at": "...", "updated_at": "..." }` |
| `400 Bad Request` | Validation error or user already has a factory | `{ "error": "User already has a factory" }` or `{ "error": "Factory name is required" }` |
| `401 Unauthorized` | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }`
| `404 Not Found` | User not found | `{ "error": "User not found" }` |

---

### 5. Update Factory

**`PUT /api/factories/update/{factory_id}`**

#### Description
Fully update an existing factory's information (name, location, description, etc.).

#### Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

#### Request Body (JSON)
```json
{
  "name": "Updated Factory Name",
  "location": "Bizerte, Tunisia",
  "description": "Modernized production facility with new equipment"
}
```

#### Response

| Status | Description | Body |
|--------|-------------|------|
| `200 OK` | Factory updated successfully | `{ "id": 1, "name": "Updated Factory Name", "location": "Bizerte, Tunisia", "description": "Modernized production facility with new equipment", "user_id": 5, "updated_at": "2025-11-04T15:30:00Z" }` |
| `400 Bad Request` | Invalid data | `{ "error": "Factory name is required" }` |
| `401 Unauthorized` | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` 
| `404 Not Found` | Factory not found | `{ "error": "Factory not found" }` |

---

### 6. Delete Factory

**`DELETE /api/factories/delete/{factory_id}`**

#### Description
Delete a factory and all related data (machines, reports, notifications, etc.).

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Cascade Behavior
Deleting a factory will permanently remove:
- All machines associated with the factory
- All reports generated for the factory
- All notifications related to the factory
- All other related data

#### Response

| Status | Description | Body |
|--------|-------------|------|
| `204 No Content` | Factory deleted successfully | — |
| `401 Unauthorized` | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` 
| `404 Not Found` | Factory not found | `{ "error": "Factory not found" }` |

---

## 🔐 Authorization Rules

### Admin Users
- Can view all factories
- Can create factories for any client
- Can update any factory
- Can delete any factory

### Client Users
- Can only view their own factory
- Cannot create additional factories (one factory per client)
- Can update their own factory information
- Cannot delete their factory (admin action required)

---

## 📝 Notes

- Each client user is associated with exactly **one factory**.
- Factory deletion is a cascading operation that removes all dependent data.
- The `owner_id` field links the factory to its owner (client user).
- Admins have full CRUD access to all factories across the system.