# 🧾 Reports API Contract

## Overview
The Reports API manages periodic reports for factories. Reports track factory performance and activities over daily, weekly, or monthly periods and can include downloadable PDF files.

## Base URL
```
/api/reports
```

## Authentication
All endpoints require authentication via JWT Bearer token.

### Request Headers
```
Authorization: Bearer <jwt_token>
```

---

## 📘 Endpoints

### 1. Get All Reports
**GET** `/api/reports`

#### Description
Retrieves a list of all reports in the system (admin view). Supports filtering by factory, period, and date range.

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
    "period": "monthly",
    "start_date": "2025-10-01",
    "end_date": "2025-10-31",
    "file_path": "/reports/factory_5_monthly_2025_10.pdf",
    "created_at": "2025-11-01T08:00:00Z"
  },
  {
    "id": 2,
    "factory_id": 5,
    "period": "weekly",
    "start_date": "2025-10-21",
    "end_date": "2025-10-27",
    "file_path": "/reports/factory_5_weekly_2025_w43.pdf",
    "created_at": "2025-10-28T09:00:00Z"
  }
]
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 200 OK | Reports retrieved successfully | Array of report objects |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |

---

### 2. Get Report by ID
**GET** `/api/reports/{id}`

#### Description
Fetches a single report by its ID, including all details (factory, period, file path, etc.).

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Response
```json
{
  "id": 1,
  "factory_id": 5,
  "period": "monthly",
  "start_date": "2025-10-01",
  "end_date": "2025-10-31",
  "file_path": "/reports/factory_5_monthly_2025_10.pdf",
  "created_at": "2025-11-01T08:00:00Z"
}
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 200 OK | Report found | Report object |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| 404 Not Found | Report does not exist | `{ "error": "Report not found" }` |

---

### 3. Get Factory's Reports
**GET** `/api/factories/{factory_id}/reports`

#### Description
Fetches all reports belonging to a specific factory. Clients can only access their own factory's reports.

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
    "period": "monthly",
    "start_date": "2025-10-01",
    "end_date": "2025-10-31",
    "file_path": "/reports/factory_5_monthly_2025_10.pdf",
    "created_at": "2025-11-01T08:00:00Z"
  },
  {
    "id": 3,
    "factory_id": 5,
    "period": "daily",
    "start_date": "2025-10-15",
    "end_date": "2025-10-15",
    "file_path": "/reports/factory_5_daily_2025_10_15.pdf",
    "created_at": "2025-10-16T07:00:00Z"
  }
]
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 200 OK | Reports retrieved successfully | Array of report objects |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| 404 Not Found | Factory not found | `{ "error": "Factory not found" }` |

---

### 4. Create Report
**POST** `/api/reports/create`

#### Description
Creates a new report (usually triggered when a report is generated for a given period). This endpoint is typically used by system processes or administrators.

#### Headers
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

#### Request Body (JSON)
```json
{
  "factory_id": 5,
  "period": "monthly",
  "start_date": "2025-11-01",
  "end_date": "2025-11-30",
  "file_path": "/reports/factory_5_monthly_2025_11.pdf"
}
```

#### Constraints
- `factory_id` is required and must reference an existing factory
- `period` is required and must be one of: `daily`, `weekly`, `monthly`
- `start_date` is required (format: YYYY-MM-DD)
- `end_date` is required (format: YYYY-MM-DD)
- `end_date` must be equal to or after `start_date`
- `file_path` must be unique

#### Response
```json
{
  "id": 4,
  "factory_id": 5,
  "period": "monthly",
  "start_date": "2025-11-01",
  "end_date": "2025-11-30",
  "file_path": "/reports/factory_5_monthly_2025_11.pdf",
  "created_at": "2025-11-04T10:00:00Z"
}
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 201 Created | Report successfully created | Report object |
| 400 Bad Request | Validation error | `{ "error": "End date must be after start date" }` or `{ "error": "Invalid period value. Must be one of: daily, weekly, monthly" }` |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| 404 Not Found | Factory not found | `{ "error": "Factory not found" }` |

---

### 6. Delete Report
**DELETE** `/api/reports/{report_id}/delete`

#### Description
Deletes a specific report and its associated file (if applicable).

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 204 No Content | Report deleted successfully | — |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| 404 Not Found | Report not found | `{ "error": "Report not found" }` |

---

### 7. Download Report
**GET** `/api/reports/{report_id}/download`

#### Description
Downloads the PDF file linked to a report using its `file_path`. Returns the file as a binary stream.

#### Headers
```
Authorization: Bearer <jwt_token>
```

#### Response
- **Content-Type**: `application/pdf`
- **Content-Disposition**: `attachment; filename="monthly_report_2025_10.pdf"`
- **Body**: Binary PDF file stream

#### Response Codes
| Status | Description | Body |
|--------|-------------|------|
| 200 OK | File download initiated | PDF binary stream |
| 401 Unauthorized | Missing or invalid token | `{ "error": "Invalid or missing authentication token" }` |
| 404 Not Found | Report not found or file does not exist | `{ "error": "Report not found" }` or `{ "error": "Report file not available" }` |

---

## 🔐 Authorization Rules

### Admin Users
- Can view all reports across all factories
- Can delete any report
- Can download any report file
- Can view latest reports for any factory

### Client Users
- Can only view reports from their own factory
- Can delete their own factory's reports
- Can download their own factory's report files
- Can view latest report for their own factory

---

## 📝 Notes

- Valid report periods: `daily`, `weekly`, `monthly`
- Date format for all date fields: `YYYY-MM-DD`
- `end_date` must be equal to or after `start_date`
- `file_path` is optional and can be set during creation or updated later
- Deleting a factory will cascade delete all its reports
- Report files should be stored securely with appropriate access controls
- The `created_at` timestamp indicates when the report record was created, not necessarily when the PDF was generated
- Downloads use binary streaming for efficiency with large PDF files
- Latest report queries are based on `created_at` timestamp (most recent creation)