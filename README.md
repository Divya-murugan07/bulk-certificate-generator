
# Bulk Certificate Generator API

## Overview
The Bulk Certificate Generator API is a Python-based backend application that generates PDF certificates for multiple recipients through a single API request. It validates recipient information, tracks job status, records individual certificate results, and supports downloading generated certificates.

## Features
- Bulk certificate generation from one request
- Recipient name and email validation
- PDF certificate generation using ReportLab
- Background processing of generation jobs
- Job status and success/failure tracking
- Individual certificate result retrieval
- PDF certificate download
- SQLite relational database storage
- Automated API tests using pytest

## Technologies Used
- Python
- FastAPI
- SQLite
- SQLAlchemy
- ReportLab
- Pydantic
- Pytest

## Project Structure
```text
bulk-certificate-generator/
├── app/
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes.py
│   └── certificate_service.py
├── tests/
│   └── test_api.py
├── generated/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup Instructions

### 1. Clone the repository
```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd bulk-certificate-generator
```

### 2. Create a virtual environment
```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows Command Prompt:
```cmd
venv\Scripts\activate
```

Windows PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Start the API
```bash
python -m uvicorn main:app --reload
```

### 6. Open API documentation
Visit:
http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| POST | `/api/v1/jobs` | Create a bulk certificate job |
| GET | `/api/v1/jobs/{job_id}` | Check job status and progress |
| GET | `/api/v1/jobs/{job_id}/certificates` | List certificates for a job |
| GET | `/api/v1/certificates/{certificate_id}` | Download a generated PDF |

## Example Request

```json
{
  "event_name": "Python Workshop 2026",
  "certificate_title": "Certificate of Participation",
  "recipients": [
    {
      "name": "Arun Kumar",
      "email": "arun@example.com"
    },
    {
      "name": "Priya Sharma",
      "email": "priya@example.com"
    }
  ]
}
```

## Run Tests

```bash
python -m pytest -v
```

## Database Design
The application uses two relational tables:

- **Jobs:** Stores event details, certificate title, generation status, and success/failure counts.
- **Certificates:** Stores recipient details, individual generation status, file path, and error messages.

Each certificate record belongs to a job through a foreign key.

## Design Decisions
- FastAPI provides request validation and interactive API documentation.
- SQLite provides a lightweight relational database suitable for local setup and demonstration.
- SQLAlchemy manages database models and queries.
- ReportLab generates PDF certificates.
- Background tasks allow the API to return a job identifier before processing finishes.
- Per-recipient error handling allows other certificates to be processed when one certificate fails.

## Limitations
This version uses in-process background tasks and local PDF storage. A production deployment would benefit from a dedicated task queue, persistent shared storage, authentication, and stronger job-recovery mechanisms.

## License
This project is intended for educational and assessment purposes.
