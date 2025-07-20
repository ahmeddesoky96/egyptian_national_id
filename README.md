    
A Django REST API service for validating and extracting information from Egyptian National IDs.

## Features

- Egyptian National ID validation
- Data extraction (birth date, age, gender, governorate)
- API key authentication
- Rate limiting (10 requests/hour per API key)
- API call tracking
- Using Docker

## Egyptian National ID Format

Egyptian National IDs are 14-digit numbers with the following structure:


## Installation & Setup

1. **Clone the repository**
   ```
   git clone <repository-url>
   cd national_id 
   ```

2. **Build Image**
   ```
   rename .env.temp to .env
   docker-compose up --build
   ```

### Authentication

API endpoints require API key authentication. Include your API key in the request headers:

```bash
# Method 1: Authorization header
Authorization: ApiKey your-api-key-here
(create api key using admin dashboard by create api_auth and after save enter the object again and you will find the key)
# Method 2: API-Key header
API-Key: your-api-key-here 
(create api key using admin dashboard by create api_auth and after save enter the object again and you will find the key)
```

### Create API Key

1. Access Django admin: http://localhost:8000/admin/
2. Navigate to "API Authentication" → "Add API Authentication"
3. Fill in the form and save
4. Go to the API Authentication and copy the generated API key

### Endpoints

#### 1. Validate National ID
```bash
POST /api/v1/validate-id/
Content-Type: application/json
Authorization: ApiKey 1acb25866cfc40c7a6eaa0b1859b1689

{
    "national_id": "29001011234567"
}
```

**Response (Valid ID):**
```json
{
    "is_valid": true,
    "extracted_data": {
        "national_id": "29001011234567",
        "birth_date": "1990-01-01",
        "birth_year": 1990,
        "birth_month": 1,
        "birth_day": 1,
        "age": 34,
        "gender": "Female",
        "governorate_code": "12",
        "governorate_name": "Dakahlia",
        "sequential_number": "456"
    },
    "processing_time_ms": 12,
    "timestamp": "2025-07-20T15:30:45.123456Z"
}
```

**Response (Invalid ID):**
```json
{
    "is_valid": false,
    "errors": ["Invalid birth month"],
    "processing_time_ms": 8,
    "timestamp": "2025-07-20T15:30:45.123456Z"
}
```

## Rate Limiting

- **Limit**: 10 requests per hour per API key
- **Response when exceeded**: HTTP 429 Too Many Requests
- **Reset**: resets hourly

## API Call Tracking

All API calls are automatically tracked in the database for billing purposes, including:
- API key used
- Timestamp
- National ID (partially masked for privacy)
- Extracted data 
- Processing time
- Client IP and User Agent

Access tracking data via Django admin.

## Testing

Run the test:
```bash
docker-compose run web python -m unittest discover -s id_process/tests
```


