
# Bulk Certificate Generator API

A Python-based REST API that generates PDF certificates for multiple recipients through a single request. The application validates recipient details, processes certificate generation, tracks job status, and provides endpoints to retrieve and download certificates.

## Features

- Generate certificates for multiple recipients in one API request.
- Validate recipient names and email addresses.
- Generate PDF certificates using a predefined template.
- Track job status and certificate generation results.
- Store job and recipient information in a relational database.
- Handle individual certificate generation failures.
- Retrieve certificate details and download generated PDFs.
- Test API endpoints using automated tests.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API development |
| SQLite | Relational database |
| SQLAlchemy | Database operations and ORM |
| Pydantic | Request validation |
| ReportLab | PDF certificate generation |
| Pytest | Automated testing |

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

## Prerequisites

- Python 3.10 or later
- pip
- Git

## Installation and Setup

### 1. Clone the repository

Replace `YOUR-USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR-USERNAME/bulk-certificate-generator.git
cd bulk-certificate-generator
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

**Windows Command Prompt:**

```cmd
venv\Scripts\activate
```

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the API server

```bash
python -m uvicorn main:app --reload
```

### 6. Open the API documentation

Visit the following URL in your browser:

http://127.0.0.1:8000/docs

The Swagger UI page allows you to execute and test the API endpoints.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Returns the welcome message |
| GET | `/health` | Checks API health |
| POST | `/api/v1/jobs` | Creates a bulk certificate generation job |
| GET | `/api/v1/jobs/{job_id}` | Retrieves job status and counts |
| GET | `/api/v1/jobs/{job_id}/certificates` | Lists certificates belonging to a job |
| GET | `/api/v1/certificates/{certificate_id}` | Downloads an individual PDF certificate |

## Example Request

Use `POST /api/v1/jobs` with the following JSON body:

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

A successful request returns a job ID and the total number of recipients submitted. Use the returned job ID to check the generation status and retrieve certificate records.

## Running Automated Tests

Run the tests from the project root:

```bash
python -m pytest -v
```

The test suite checks the health endpoint, bulk job creation, job status, certificate retrieval and download, invalid email validation, and handling of missing job IDs.

## Database Design

The application uses SQLite with two main tables.

### Jobs

Stores the event name, certificate title, job status, total recipient count, successful generation count, failed generation count, and creation timestamp.

### Certificates

Stores each recipient's name, email address, generation status, PDF file path, error details, and associated job ID.

A foreign key links each certificate record to its parent job.

## Design Decisions

- **FastAPI:** Provides REST endpoints, request validation, and interactive documentation.
- **SQLite:** Offers simple relational data storage for local development.
- **SQLAlchemy:** Maps Python models to database tables and manages database queries.
- **ReportLab:** Generates downloadable PDF certificates from a predefined layout.
- **BackgroundTasks:** Allows certificate generation to run after a job request is accepted.
- **Per-recipient error handling:** Records individual failures so one failed certificate does not automatically stop the remaining recipients.

## Limitations and Future Improvements

- Introduce a dedicated task queue for reliable background processing at larger scales.
- Add authentication and authorization.
- Support configurable certificate templates and branding.
- Store generated PDFs in cloud storage for deployment across multiple servers.
- Add pagination for large certificate lists.
- Improve job recovery and monitoring for production use.

## License

This project is licensed under the MIT License.

## Author

Divya Murugan
