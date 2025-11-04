# ⚙️ Machines API Contract

## Overview
The Machines API manages machine configurations and operations for factories. Each machine belongs to a factory and tracks its status, maintenance, and operational logs.

## Base URL
```
/api/machines
```

## Authentication
All endpoints require authentication via JWT Bearer token.

### Request Headers
```
Authorization: Bearer <jwt_token>
```

---

## 📘 Endpoints

### 1. Get All Machines
**GET** `/api/machines`

#### Description
Retrieves a list of all machines in the system. Admins can view all machines; clients see only their factory's machines.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Response
```json
[
  {
    "id": 1,
    "factory_id": 5,
    "name": "CNC Machine 01",
    "serial_number": "SN-12345",
    "status": "Running",
    "last_maintenance_date": "2025-10-15",
    "description": "High-precision CNC machine",
    "created_at": "2025-11-01T08:00:00Z",
    "updated_at": "2025-11-04T10:00:00Z"
  },
  {
    "id": 2,
    "factory_id": 5,
    "name": "Lathe Machine 02",
    "serial_number": "SN-67890",
    "status": "Maintenance",
    "last_maintenance_date": "2025-11-03",
    "description": "Industrial lathe machine",
    "created_at": "2025-11-02T09:30:00Z",
    "updated_at": "2025-11-03T14:20:00Z"
  }
]
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 200 OK | Machines retrieved successfully | Array of machine objects |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |

---

### 2. Get Machine by ID
**GET** `/api/machines/{machine_id}`

#### Description
Retrieves detailed information about a specific machine by its ID.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Response
```json
{
  "id": 1,
  "factory_id": 5,
  "name": "CNC Machine 01",
  "serial_number": "SN-12345",
  "status": "Running",
  "last_maintenance_date": "2025-10-15",
  "description": "High-precision CNC machine",
  "created_at": "2025-11-01T08:00:00Z",
  "updated_at": "2025-11-04T10:00:00Z"
}
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 200 OK | Machine found | Machine object |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| 404 Not Found | Machine does not exist | `{ "error": "Machine not found" }` |

---

### 3. Get Factory's Machines
**GET** `/api/machines/factory/{factory_id}`

#### Description
Lists all machines belonging to a specific factory.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Response
```json
[
  {
    "id": 1,
    "factory_id": 5,
    "name": "CNC Machine 01",
    "serial_number": "SN-12345",
    "status": "Running",
    "last_maintenance_date": "2025-10-15",
    "description": "High-precision CNC machine",
    "created_at": "2025-11-01T08:00:00Z",
    "updated_at": "2025-11-04T10:00:00Z"
  }
]
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 200 OK | Machines retrieved successfully | Array of machine objects |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| 404 Not Found | Factory not found | `{ "error": "Factory not found" }` |

---

### 4. Create Machine
**POST** `/api/machines/create/{factory_id}`

#### Description
Creates a new machine under a specific factory.

#### Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

#### Request Body (JSON)
```json
{
  "name": "CNC Machine 01",
  "serial_number": "SN-12345",
  "status": "Idle",
  "last_maintenance_date": "2025-10-15",
  "description": "High-precision CNC machine"
}
```

#### Constraints
- `factory_id` must reference an existing factory
- `name` must be unique across all machines
- `serial_number` must be unique across all machines
- `name` and `serial_number` are required
- `status` must be one of: `Running`, `Idle`, `Maintenance`, `Stopped` (defaults to `Idle`)
- `last_maintenance_date` format: `YYYY-MM-DD`
- `description` is optional

#### Response
```json
{
  "id": 1,
  "factory_id": 5,
  "name": "CNC Machine 01",
  "serial_number": "SN-12345",
  "status": "Idle",
  "last_maintenance_date": "2025-10-15",
  "description": "High-precision CNC machine",
  "created_at": "2025-11-04T10:00:00Z",
  "updated_at": "2025-11-04T10:00:00Z"
}
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 201 Created | Machine successfully created | Machine object |
| 400 Bad Request | Validation error | `{ "error": "Machine name must be unique" }` or `{ "error": "Serial number already exists" }` or `{ "error": "Invalid status value" }` |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| 404 Not Found | Factory not found | `{ "error": "Factory not found" }` |

---

### 5. Update Machine
**PUT** `/api/machines/{machine_id}/update`

#### Description
Updates an existing machine's information (name, status, description, maintenance date, etc.).

#### Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

#### Request Body (JSON)
```json
{
  "name": "Updated CNC Machine 01",
  "serial_number": "SN-12345-NEW",
  "status": "Running",
  "last_maintenance_date": "2025-11-01",
  "description": "Updated high-precision CNC machine"
}
```

#### Constraints
- `name` must be unique if changed
- `serial_number` must be unique if changed
- `status` must be one of: `Running`, `Idle`, `Maintenance`, `Stopped`
- `last_maintenance_date` format: `YYYY-MM-DD`

#### Response
```json
{
  "id": 1,
  "factory_id": 5,
  "name": "Updated CNC Machine 01",
  "serial_number": "SN-12345-NEW",
  "status": "Running",
  "last_maintenance_date": "2025-11-01",
  "description": "Updated high-precision CNC machine",
  "created_at": "2025-11-01T08:00:00Z",
  "updated_at": "2025-11-04T15:30:00Z"
}
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 200 OK | Machine updated successfully | Machine object |
| 400 Bad Request | Validation error | `{ "error": "Machine name must be unique" }` or `{ "error": "Invalid status value" }` |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| 404 Not Found | Machine not found | `{ "error": "Machine not found" }` |

---

### 6. Update Machine Status
**PATCH** `/api/machines/{machine_id}/update/status`

#### Description
Updates only the machine's operational status (e.g., from `Running` → `Maintenance`). This is a lightweight endpoint for status changes without requiring full machine details.

#### Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

#### Request Body (JSON)
```json
{
  "status": "Maintenance"
}
```

#### Constraints
- `status` is required
- `status` must be one of: `Running`, `Idle`, `Maintenance`, `Stopped`

#### Response
```json
{
  "id": 1,
  "factory_id": 5,
  "name": "CNC Machine 01",
  "serial_number": "SN-12345",
  "status": "Maintenance",
  "last_maintenance_date": "2025-10-15",
  "description": "High-precision CNC machine",
  "created_at": "2025-11-01T08:00:00Z",
  "updated_at": "2025-11-04T16:00:00Z"
}
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 200 OK | Status updated successfully | Machine object |
| 400 Bad Request | Invalid status value | `{ "error": "Invalid status value. Must be one of: Running, Idle, Maintenance, Stopped" }` |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| 404 Not Found | Machine not found | `{ "error": "Machine not found" }` |

---

### 7. Delete Machine
**DELETE** `/api/machines/{machine_id}/delete`

#### Description
Deletes a machine and automatically removes its logs and notifications (via cascade).

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 204 No Content | Machine deleted successfully | — |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| 404 Not Found | Machine not found | `{ "error": "Machine not found" }` |

---

### 8. Get Machine Logs
**GET** `/api/machines/{machine_id}/logs`

#### Description
Retrieves all log entries associated with a machine (from the Machine Logs table).

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Response
```json
[
  {
    "id": 1,
    "machine_id": 1,
    "timestamp": "2025-11-04T10:30:00Z",
    "status": "Running",
    "notes": "Machine started after maintenance"
  },
  {
    "id": 2,
    "machine_id": 1,
    "timestamp": "2025-11-04T14:15:00Z",
    "status": "Idle",
    "notes": "Paused for shift break"
  }
]
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 200 OK | Logs retrieved successfully | Array of log objects |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| 404 Not Found | Machine not found | `{ "error": "Machine not found" }` |

---

### 9. Create Machine Log
**POST** `/api/machines/{machine_id}/logs/create`

#### Description
Adds a new log entry for a machine (status change, remark, or system event).

#### Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

#### Request Body (JSON)
```json
{
  "status": "Maintenance",
  "notes": "Scheduled maintenance completed"
}
```

#### Constraints
- `status` is required and must be one of: `Running`, `Idle`, `Maintenance`, `Fault`
- `notes` is optional
- `timestamp` is automatically set to current time

#### Response
```json
{
  "id": 3,
  "machine_id": 1,
  "timestamp": "2025-11-04T16:45:00Z",
  "status": "Maintenance",
  "notes": "Scheduled maintenance completed"
}
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 201 Created | Log entry created successfully | Log object |
| 400 Bad Request | Invalid status value | `{ "error": "Invalid status value. Must be one of: Running, Idle, Maintenance, Fault" }` |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| 404 Not Found | Machine not found | `{ "error": "Machine not found" }` |

---


## 🔐 Authorization Rules

### Admin Users
- Can view all machines across all factories
- Can create machines for any factory
- Can update any machine
- Can delete any machine
- Can view and create logs for any machine
- Can filter machines by status across all factories

### Client Users
- Can only view machines from their own factory
- Can create machines for their own factory
- Can update their own factory's machines
- Can delete their own factory's machines
- Can view and create logs for their own factory's machines
- Can filter machines by status (limited to their factory)

---

## 📝 Notes

- Machine `name` and `serial_number` must be unique across the entire system
- Valid machine statuses: `Running`, `Idle`, `Maintenance`, `Stopped`
- Valid log statuses: `Running`, `Idle`, `Maintenance`, `Fault`
- Deleting a machine will cascade delete its logs and notifications
- All timestamps are in ISO 8601 format with UTC timezone
- `last_maintenance_date` is stored in DATE format (YYYY-MM-DD)
- Machine logs are automatically timestamped on creation
- Status updates via PATCH endpoint only affect the `status` field; use PUT for full updates