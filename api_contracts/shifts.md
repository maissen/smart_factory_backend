# 🕒 Shift API Contract

## Overview

The Shift API manages shift configurations for factories. Each factory has exactly one shift configuration that defines working hours and scheduling information.

### Base URL
```
/api/shifts
```

### Authentication
All endpoints require authentication via JWT Bearer token.

#### Request Headers
```
Authorization: Bearer <jwt_token>
```

---

## 📘 Endpoints

### 1. Get All Shifts

**`GET /api/shifts`**

#### Description
Retrieves a list of all shifts in the system (admin view).

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Example
```
GET /api/shifts
```

#### Response
```json
[
  {
    "id": 1,
    "factory_id": 5,
    "name": "Day Shift",
    "start_time": "08:00:00",
    "end_time": "16:00:00",
    "created_at": "2025-11-04T10:00:00Z",
    "updated_at": "2025-11-04T10:00:00Z"
  },
  {
    "id": 2,
    "factory_id": 8,
    "name": "Morning Shift",
    "start_time": "06:00:00",
    "end_time": "14:00:00",
    "created_at": "2025-11-03T14:30:00Z",
    "updated_at": "2025-11-03T14:30:00Z"
  }
]
```

#### Response Codes

| Status | Description | Body |
|--------|-------------|------|
| `200 OK` | Shifts retrieved successfully | Array of shift objects |
| `401 Unauthorized` | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |

---

### 2. Get Shift by ID

**`GET /api/shifts/{shift_id}`**

#### Description
Retrieves detailed information about a specific shift by its ID (for admin or debugging).

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Example
```
GET /api/shifts/1
```

#### Response

```json
{
  "id": 1,
  "factory_id": 5,
  "name": "Day Shift",
  "start_time": "08:00:00",
  "end_time": "16:00:00",
  "created_at": "2025-11-04T10:00:00Z",
  "updated_at": "2025-11-04T10:00:00Z"
}
```

#### Response Codes

| Status | Description | Body |
|--------|-------------|------|
| `200 OK` | Shift found | Shift object |
| `401 Unauthorized` | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| `404 Not Found` | Shift does not exist | `{ "error": "Shift not found" }` |

---

### 3. Get Factory's Shift

**`GET /api/factories/{factory_id}/shift`**

#### Description
Retrieves the shift configuration for a specific factory. Since each factory has only one shift, this returns a single record.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Example
```
GET /api/factories/5/shift
```

#### Response

```json
{
  "id": 1,
  "factory_id": 5,
  "name": "Day Shift",
  "start_time": "08:00:00",
  "end_time": "16:00:00",
  "created_at": "2025-11-04T10:00:00Z",
  "updated_at": "2025-11-04T10:00:00Z"
}
```

#### Response Codes

| Status | Description | Body |
|--------|-------------|------|
| `200 OK` | Shift found | Shift object |
| `401 Unauthorized` | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` 
| `404 Not Found` | Factory has no shift or factory not found | `{ "error": "Shift not found for this factory" }` |

---

### 4. Create Factory Shift

**`POST /api/shifts/create/{factory_id}`**

#### Description
Creates a new shift for a factory. Only one shift is allowed per factory.

#### Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

#### Request Body (JSON)
```json
{
  "name": "Day Shift",
  "start_time": "08:00:00",
  "end_time": "16:00:00"
}
```

#### Constraints
* `factory_id` must reference an existing factory.
* Each factory can have only one shift.
* `name`, `start_time`, and `end_time` are required.
* `start_time` must be before `end_time`.
* Time format: `HH:MM:SS` (24-hour format).

#### Responses

| Status | Description | Body |
|--------|-------------|------|
| `201 Created` | Shift successfully created | `{ "id": 1, "factory_id": 5, "name": "Day Shift", "start_time": "08:00:00", "end_time": "16:00:00", "created_at": "...", "updated_at": "..." }` |
| `400 Bad Request` | Validation error or factory already has a shift | `{ "error": "Factory already has a shift" }` or `{ "error": "Start time must be before end time" }` |
| `401 Unauthorized` | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| `404 Not Found` | Factory not found | `{ "error": "Factory not found" }` |

---

### 5. Update Factory Shift

**`PUT /api/shifts/update/{factory_id}`**

#### Description
Updates the existing shift configuration for a factory (e.g., name, start time, end time).

#### Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

#### Request Body (JSON)
```json
{
  "name": "Updated Day Shift",
  "start_time": "07:00:00",
  "end_time": "15:00:00"
}
```

#### Constraints
* `start_time` must be before `end_time`.
* Time format: `HH:MM:SS` (24-hour format).

#### Response

| Status | Description | Body |
|--------|-------------|------|
| `200 OK` | Shift updated successfully | `{ "id": 1, "factory_id": 5, "name": "Updated Day Shift", "start_time": "07:00:00", "end_time": "15:00:00", "updated_at": "2025-11-04T15:30:00Z" }` |
| `400 Bad Request` | Invalid data | `{ "error": "Start time must be before end time" }` or `{ "error": "Invalid time format" }` |
| `401 Unauthorized` | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| `404 Not Found` | Shift not found for this factory | `{ "error": "Shift not found for this factory" }` |

---

### 6. Delete Factory Shift

**`DELETE /api/shifts/delete/{factory_id}`**

#### Description
Deletes the shift associated with a given factory.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Response

| Status | Description | Body |
|--------|-------------|------|
| `204 No Content` | Shift deleted successfully | — |
| `401 Unauthorized` | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| `404 Not Found` | Shift not found | `{ "error": "Shift not found for this factory" }` |

---

## 🔐 Authorization Rules

### Admin Users
- Can view all shifts across all factories
- Can create shifts for any factory
- Can update any shift
- Can delete any shift

### Client Users
- Can only view their own factory's shift
- Can create a shift for their factory (if none exists)
- Can update their own factory's shift
- Can delete their own factory's shift

---

## 📝 Notes

- Each factory has exactly **one shift configuration**.
- The `factory_id` in the shifts table has a `UNIQUE` constraint to enforce the one-to-one relationship.
- Time values must be in 24-hour format (`HH:MM:SS`).
- `start_time` must always be before `end_time`.
- Deleting a factory will cascade delete its associated shift.
- Shift times are stored in TIME format without timezone information.