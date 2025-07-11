# Python MCP Template
Version: 0.1.0
A template for creating MCP-compliant FastAPI services.

## /new/endpoint/

### POST

**Summary:** New Endpoint

**Request Body:**

Content-Type: `application/json`

Schema:
[NewEndpointRequest](#schema-newendpointrequest)

**Responses:**

**200**: Successful Response

Content-Type: `application/json`

Schema:
[NewEndpointResponse](#schema-newendpointresponse)

**422**: Validation Error

Content-Type: `application/json`

Schema:
[HTTPValidationError](#schema-httpvalidationerror)

---

# Data Models

## Schema: HTTPValidationError

**Schema:**
```json
{
  "detail": [ValidationError]  // 
}
```

**Properties:**

- **detail**: `[ValidationError]`

---

## Schema: NewEndpointRequest

**Schema:**
```json
{
  "name": string (required)  // The name to include in the message.
}
```

**Properties:**

- **name** *(required)*: `string`
  - Description: The name to include in the message.
  - Example: `developer`

---

## Schema: NewEndpointResponse

**Schema:**
```json
{
  "message": string (required)  // A welcome message.
}
```

**Properties:**

- **message** *(required)*: `string`
  - Description: A welcome message.
  - Example: `Hello, world!`

---

## Schema: ValidationError

**Schema:**
```json
{
  "loc": [unknown] (required)  // 
  "msg": string (required)  // 
  "type": string (required)  // 
}
```

**Properties:**

- **loc** *(required)*: `[unknown]`

- **msg** *(required)*: `string`

- **type** *(required)*: `string`

---
