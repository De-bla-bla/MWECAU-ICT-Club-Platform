# API Documentation

## Overview

The MWECAU ICT Club API provides RESTful endpoints for accessing and managing club data. Authentication is required for most endpoints.

## Base URL

```
https://api.yourdomain.com/api/
```

## Authentication

The API uses token-based authentication. Include your token in the Authorization header:

```
Authorization: Bearer YOUR_TOKEN_HERE
```

Or use session authentication for web-based clients.

## Response Format

All responses are in JSON format with the following structure:

```json
{
  "data": {},
  "status": "success",
  "message": "Operation completed successfully"
}
```

## Error Responses

Error responses include an error code and message:

```json
{
  "error": "NOT_FOUND",
  "message": "Resource not found",
  "status": 404
}
```

## Endpoints

### Departments

#### List Departments
```
GET /departments/
```

Query Parameters:
- `search`: Search by name or description
- `ordering`: Sort by field (name, created_at)
- `page`: Page number (default: 1)

Response:
```json
{
  "count": 6,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Programming",
      "slug": "programming",
      "description": "Programming department",
      "member_count": 25
    }
  ]
}
```

#### Get Department
```
GET /departments/{id}/
```

### Courses

#### List Courses
```
GET /courses/
```

Query Parameters:
- `department`: Filter by department ID
- `search`: Search by name or code
- `ordering`: Sort by field

#### Get Course
```
GET /courses/{id}/
```

### Users

#### Get Current User Profile
```
GET /users/profile/
```

Response:
```json
{
  "id": 1,
  "reg_number": "SE2021001",
  "email": "user@example.com",
  "full_name": "John Doe",
  "department": 1,
  "department_name": "Programming",
  "is_approved": true,
  "role": "Member"
}
```

#### List Users (Admin Only)
```
GET /users/
```

Query Parameters:
- `department`: Filter by department
- `is_approved`: Filter by approval status
- `search`: Search by name, email, or reg_number

#### Approve User (Admin Only)
```
POST /users/{id}/approve/
```

#### Reject User (Admin Only)
```
POST /users/{id}/reject/
```

### Projects

#### List Projects
```
GET /projects/
```

Query Parameters:
- `department`: Filter by department
- `featured`: Filter featured projects (true/false)
- `search`: Search by title or description
- `ordering`: Sort by field

#### Get Project
```
GET /projects/{id}/
```

#### Get Featured Projects
```
GET /projects/featured/
```

### Events

#### List Events
```
GET /events/
```

Query Parameters:
- `department`: Filter by department
- `search`: Search by title, description, or location

#### Get Event
```
GET /events/{id}/
```

#### Get Upcoming Events
```
GET /events/upcoming/
```

### Announcements

#### List Announcements
```
GET /announcements/
```

Query Parameters:
- `announcement_type`: Filter by type
- `department`: Filter by department
- `search`: Search by title or content

#### Get Announcement
```
GET /announcements/{id}/
```

#### Get Recent Announcements
```
GET /announcements/recent/
```

Returns last 10 announcements.

#### Get Urgent Announcements
```
GET /announcements/urgent/
```

### Payments

#### List User Payments
```
GET /payments/my_payments/
```

#### Get Payment Details
```
GET /payments/{id}/
```

#### Create Payment
```
POST /payments/
```

Request body:
```json
{
  "user": 1,
  "amount": 15000,
  "provider": "mpesa",
  "transaction_id": "ABC123"
}
```

#### Confirm Payment (Admin Only)
```
POST /payments/{id}/confirm_payment/
```

## Rate Limiting

API requests are limited to 100 requests per hour per IP address.

## Pagination

List endpoints support pagination:

```
GET /endpoint/?page=2&page_size=20
```

Default page size is 20. Maximum is 100.

## Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created
- `204 No Content`: Request successful, no content to return
- `400 Bad Request`: Invalid request
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Server Error`: Server error

## Examples

### Get all approved users in Programming department
```
GET /users/?department=1&is_approved=true
```

### Search for projects
```
GET /projects/?search=website&ordering=-created_at
```

### Get current user's recent activities
```
GET /users/profile/
```

## Webhooks

Webhook support for payment confirmations and member approvals is available. Contact admin for setup.

## Support

For API support and questions, contact: api@yourdomain.com
