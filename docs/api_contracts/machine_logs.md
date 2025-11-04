# 📜 Machine Logs API Contract

## Overview
The Machine Logs API tracks machine state changes and important remarks. Each log entry captures a timestamp, status, and optional notes to maintain a complete activity timeline for every machine.

## Base URL
```
/api/machine-logs
```

## Authentication
All endpoints require authentication via JWT Bearer token.

### Request Headers
```
Authorization: Bearer <jwt_token>
```

---

## 📘 Endpoints

### 1. Get All Machine Logs
**GET** `/api/machine-logs/{factory_id}`

#### Description
Fetches all machine logs in the system. Admins can see all logs; clients see only logs for machines in their factory. Can be filtered by query parameters.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Response
```json
[
  {
    "id": 1,
    "machine_id": 3,
    "timestamp": "2025-11-04T10:30:00Z",
    "status": "Fault",
    "notes": "CNC Machine 01 stopped unexpectedly - electrical fault detected"
  },
  {
    "id": 2,
    "machine_id": 3,
    "timestamp": "2025-11-04T08:15:00Z",
    "status": "Running",
    "notes": "Machine restarted after maintenance"
  }
]
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 200 OK | Logs retrieved successfully | Array of log objects |
| 400 Bad Request | Invalid query parameters | `{ "error": "Invalid status value" }` or `{ "error": "Invalid date format" }` |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |

---

### 2. Get Machine Logs by Machine ID
**GET** `/api/machines/{machine_id}/logs`

#### Description
Fetches all logs related to a specific machine. Used to display its activity timeline or history.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Path Parameters
| Parameter | Type | Description |
|-----------|------|-------------|
| `machine_id` | Integer | The ID of the machine |

#### Response
```json
[
  {
    "id": 1,
    "machine_id": 3,
    "timestamp": "2025-11-04T10:30:00Z",
    "status": "Fault",
    "notes": "CNC Machine 01 stopped unexpectedly - electrical fault detected"
  },
  {
    "id": 2,
    "machine_id": 3,
    "timestamp": "2025-11-04T08:15:00Z",
    "status": "Running",
    "notes": "Machine restarted after maintenance"
  },
  {
    "id": 3,
    "machine_id": 3,
    "timestamp": "2025-11-03T16:45:00Z",
    "status": "Maintenance",
    "notes": "Scheduled maintenance - oil change and calibration"
  }
]
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 200 OK | Logs retrieved successfully | Array of log objects |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| 403 Forbidden | Client accessing another factory's machine logs | `{ "error": "Access denied" }` |
| 404 Not Found | Machine not found | `{ "error": "Machine not found" }` |

---

### 3. Create Machine Log
**POST** `/api/machine-logs/create`

#### Description
Creates a new machine log entry. This can be triggered automatically by system events (status changes) or manually by users to add maintenance notes or remarks.

#### Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

#### Request Body (JSON)
```json
{
  "machine_id": 3,
  "status": "Maintenance",
  "notes": "Scheduled maintenance - replaced worn bearings"
}
```

#### Constraints
- `machine_id` is required and must reference an existing machine
- `status` is required and must be one of: `Running`, `Idle`, `Maintenance`, `Fault`
- `notes` is optional (text field)
- `timestamp` is automatically set to current time

#### Response
```json
{
  "id": 15,
  "machine_id": 3,
  "timestamp": "2025-11-04T10:30:00Z",
  "status": "Maintenance",
  "notes": "Scheduled maintenance - replaced worn bearings"
}
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 201 Created | Log entry created successfully | Log object |
| 400 Bad Request | Validation error | `{ "error": "Machine ID is required" }` or `{ "error": "Invalid status value" }` |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| 403 Forbidden | Client creating log for another factory's machine | `{ "error": "Access denied" }` |
| 404 Not Found | Machine not found | `{ "error": "Machine not found" }` |

---

## 🔐 Authorization Rules

### Admin Users
- Can view all machine logs across all factories

### Client Users
- Can only view logs for machines in their own factory

---

## 📝 Notes

- Machine logs are ordered by `timestamp` (newest first) by default
- Logs are automatically created when machine status changes occur
- The `status` field must match one of the valid machine statuses: `Running`, `Idle`, `Maintenance`, `Fault`
- `notes` are optional and can contain system-generated remarks or user comments
- All timestamps are in ISO 8601 format with UTC timezone
- Logs provide a complete audit trail of machine activity
- Logs cannot be modified after creation (append-only for audit purposes)