# 🔔 Notifications API Contract

## Overview
The Notifications API manages in-app alerts for users. Notifications can be linked to factories or machines and track important events like machine faults, maintenance alerts, and system updates.

## Base URL
```
/api/notifications
```

## Authentication
All endpoints require authentication via JWT Bearer token.

### Request Headers
```
Authorization: Bearer <jwt_token>
```

---

## 📘 Endpoints

### 1. Get All Notifications
**GET** `/api/notifications`

#### Description
Fetches all notifications. Admins can see all notifications across the system; clients see only their own notifications.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Response
```json
[
  {
    "id": 1,
    "user_id": 10,
    "factory_id": 5,
    "machine_id": 3,
    "type": "Machine Fault",
    "message": "CNC Machine 01 has stopped unexpectedly",
    "is_read": false,
    "created_at": "2025-11-04T10:30:00Z"
  },
  {
    "id": 2,
    "user_id": 10,
    "factory_id": 5,
    "machine_id": null,
    "type": "Maintenance Alert",
    "message": "Scheduled maintenance due for Factory A",
    "is_read": true,
    "created_at": "2025-11-03T14:15:00Z"
  }
]
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 200 OK | Notifications retrieved successfully | Array of notification objects |
| 400 Bad Request | Invalid query parameters | `{ "error": "Invalid is_read value" }` |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |

---

### 2. Get Notification by ID
**GET** `/api/notifications/{id}`

#### Description
Fetches details of a specific notification by its ID.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Response
```json
{
  "id": 1,
  "user_id": 10,
  "factory_id": 5,
  "machine_id": 3,
  "type": "Machine Fault",
  "message": "CNC Machine 01 has stopped unexpectedly",
  "is_read": false,
  "created_at": "2025-11-04T10:30:00Z"
}
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 200 OK | Notification found | Notification object |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| 403 Forbidden | Client accessing another user's notification | `{ "error": "Access denied" }` |
| 404 Not Found | Notification does not exist | `{ "error": "Notification not found" }` |

---

### 4. Get Factory Notifications
**GET** `/api/notifications/factory/{factory_id}`

#### Description
Fetches all notifications related to a specific factory.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Response
```json
[
  {
    "id": 1,
    "user_id": 10,
    "factory_id": 5,
    "machine_id": 3,
    "type": "Machine Fault",
    "message": "CNC Machine 01 has stopped unexpectedly",
    "is_read": false,
    "created_at": "2025-11-04T10:30:00Z"
  },
  {
    "id": 2,
    "user_id": 10,
    "factory_id": 5,
    "machine_id": null,
    "type": "Maintenance Alert",
    "message": "Scheduled maintenance due for Factory A",
    "is_read": true,
    "created_at": "2025-11-03T14:15:00Z"
  }
]
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 200 OK | Notifications retrieved successfully | Array of notification objects |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| 403 Forbidden | Client accessing another factory's notifications | `{ "error": "Access denied" }` |
| 404 Not Found | Factory not found | `{ "error": "Factory not found" }` |

---

### 5. Get Machine Notifications
**GET** `/api/notifications/machine/{machine_id}`

#### Description
Fetches all notifications related to a specific machine.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Response
```json
[
  {
    "id": 1,
    "user_id": 10,
    "factory_id": 5,
    "machine_id": 3,
    "type": "Machine Fault",
    "message": "CNC Machine 01 has stopped unexpectedly",
    "is_read": false,
    "created_at": "2025-11-04T10:30:00Z"
  },
  {
    "id": 8,
    "user_id": 10,
    "factory_id": 5,
    "machine_id": 3,
    "type": "Status Change",
    "message": "CNC Machine 01 status changed to Maintenance",
    "is_read": true,
    "created_at": "2025-11-02T11:20:00Z"
  }
]
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 200 OK | Notifications retrieved successfully | Array of notification objects |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| 403 Forbidden | Client accessing another factory's machine notifications | `{ "error": "Access denied" }` |
| 404 Not Found | Machine not found | `{ "error": "Machine not found" }` |

---

### 6. Create Notification
**POST** `/api/notifications/create`

#### Description
Creates a new notification. This can be triggered automatically by system events or manually by an admin.

#### Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

#### Request Body (JSON)
```json
{
  "user_id": 10,
  "factory_id": 5,
  "machine_id": 3,
  "type": "Machine Fault",
  "message": "CNC Machine 01 has stopped unexpectedly"
}
```

#### Constraints
- `user_id` is required and must reference an existing user
- `factory_id` is required and must reference an existing factory
- `machine_id` is optional (for factory-level notifications)
- `type` is required (max 50 characters)
- `message` is required
- `is_read` defaults to `false`
- `created_at` is automatically set

#### Response
```json
{
  "id": 1,
  "user_id": 10,
  "factory_id": 5,
  "machine_id": 3,
  "type": "Machine Fault",
  "message": "CNC Machine 01 has stopped unexpectedly",
  "is_read": false,
  "created_at": "2025-11-04T10:30:00Z"
}
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 201 Created | Notification successfully created | Notification object |
| 400 Bad Request | Validation error | `{ "error": "User ID is required" }` or `{ "error": "Message cannot be empty" }` |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| 403 Forbidden | Insufficient permissions | `{ "error": "Access denied" }` |
| 404 Not Found | User, factory, or machine not found | `{ "error": "User not found" }` or `{ "error": "Factory not found" }` or `{ "error": "Machine not found" }` |

---

### 7. Mark Notification as Read
**PATCH** `/api/notifications/{id}/read`

#### Description
Marks a specific notification as read by setting `is_read` to `true`.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Response
```json
{
  "id": 1,
  "user_id": 10,
  "factory_id": 5,
  "machine_id": 3,
  "type": "Machine Fault",
  "message": "CNC Machine 01 has stopped unexpectedly",
  "is_read": true,
  "created_at": "2025-11-04T10:30:00Z"
}
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 200 OK | Notification marked as read | Notification object |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| 403 Forbidden | Client marking another user's notification | `{ "error": "Access denied" }` |
| 404 Not Found | Notification not found | `{ "error": "Notification not found" }` |

---

### 8. Delete Notification
**DELETE** `/api/notifications/{id}/delete`

#### Description
Deletes a specific notification.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 204 No Content | Notification deleted successfully | — |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| 403 Forbidden | Client deleting another user's notification | `{ "error": "Access denied" }` |
| 404 Not Found | Notification not found | `{ "error": "Notification not found" }` |

---

### 9. Clear All Notifications
**DELETE** `/api/notifications/clear-all`

#### Description
Deletes all notifications for the current user. Use with caution as this action is irreversible.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Example
```http
DELETE /api/notifications/clear-all
```

#### Response
```json
{
  "message": "All notifications cleared",
  "deleted_count": 8
}
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 200 OK | All notifications deleted successfully | `{ "message": "All notifications cleared", "deleted_count": <number> }` |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |

---

## 🔐 Authorization Rules

### Admin Users
- Can view all notifications across all users
- Can delete any notification
- Can use clear-all

### Client Users
- Can only view their own notifications
- Cannot manually create notifications (system-generated only)
- Can mark their own notifications as read
- Can delete their own notifications
- Can clear all their own notifications

---

## 📝 Notes

- Notifications are automatically created by system events (e.g., machine faults, maintenance alerts)
- `machine_id` is optional and can be `null` for factory-level notifications
- Common notification types include: `Machine Fault`, `Maintenance Alert`, `Status Change`, `Report Ready`, `System Update`
- `type` field is flexible and not constrained to specific values (max 50 characters)
- Deleting a user will cascade delete all their notifications
- Deleting a factory will cascade delete all related notifications
- Deleting a machine will cascade delete all related notifications
- The `is_read` flag defaults to `false` for new notifications
- All timestamps are in ISO 8601 format with UTC timezone
- Notifications are ordered by `created_at` (newest first) by default
- The `updated_count` and `deleted_count` fields in bulk operations indicate how many records were affected