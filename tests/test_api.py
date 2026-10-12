from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_and_retrieve_certificates():
    payload = {
        "event_name": "Python Workshop 2026",
        "certificate_title": "Certificate of Participation",
        "recipients": [
            {
                "name": "Test User One",
                "email": "test1@example.com"
            },
            {
                "name": "Test User Two",
                "email": "test2@example.com"
            }
        ]
    }

    # Create a bulk generation job
    response = client.post("/api/v1/jobs", json=payload)

    assert response.status_code == 200

    job_id = response.json()["job_id"]

    # Check the job status
    status_response = client.get(f"/api/v1/jobs/{job_id}")

    assert status_response.status_code == 200

    job_data = status_response.json()

    assert job_data["status"] == "completed"
    assert job_data["total"] == 2
    assert job_data["successful"] == 2
    assert job_data["failed"] == 0

    # Retrieve individual certificate records
    certificates_response = client.get(
        f"/api/v1/jobs/{job_id}/certificates"
    )

    assert certificates_response.status_code == 200

    certificates = certificates_response.json()

    assert len(certificates) == 2

    # Download the first generated PDF
    certificate_id = certificates[0]["certificate_id"]

    download_response = client.get(
        f"/api/v1/certificates/{certificate_id}"
    )

    assert download_response.status_code == 200
    assert download_response.headers["content-type"] == "application/pdf"


def test_invalid_email_is_rejected():
    payload = {
        "event_name": "Python Workshop 2026",
        "certificate_title": "Certificate of Participation",
        "recipients": [
            {
                "name": "Test User",
                "email": "not-an-email"
            }
        ]
    }

    response = client.post("/api/v1/jobs", json=payload)

    assert response.status_code == 422


def test_missing_job_returns_404():
    response = client.get("/api/v1/jobs/99999999")

    assert response.status_code == 404