from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path

from app.database import get_db, SessionLocal
from app.models import Job, Certificate
from app.schemas import JobCreate
from app.certificate_service import generate_certificate

router = APIRouter(prefix="/api/v1", tags=["Certificates"])


def process_job(job_id: int):
    db = SessionLocal()

    try:
        job = db.query(Job).filter(Job.id == job_id).first()

        if not job:
            return

        job.status = "processing"
        db.commit()

        for certificate in job.certificates:
            try:
                file_path = generate_certificate(
                    recipient_name=certificate.recipient_name,
                    certificate_title=job.certificate_title,
                    event_name=job.event_name,
                    certificate_id=certificate.id,
                )

                certificate.file_path = file_path
                certificate.status = "completed"
                job.successful += 1

            except Exception as error:
                certificate.status = "failed"
                certificate.error_message = str(error)
                job.failed += 1

            db.commit()

        job.status = "completed"
        db.commit()

    except Exception:
        db.rollback()
        job.status = "failed"
        db.commit()

    finally:
        db.close()


@router.post("/jobs")
def create_job(
    data: JobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    job = Job(
        event_name=data.event_name,
        certificate_title=data.certificate_title,
        total=len(data.recipients),
        status="queued",
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    for recipient in data.recipients:
        certificate = Certificate(
            job_id=job.id,
            recipient_name=recipient.name,
            recipient_email=str(recipient.email),
            status="pending",
        )
        db.add(certificate)

    db.commit()

    background_tasks.add_task(process_job, job.id)

    return {
        "job_id": job.id,
        "status": "queued",
        "total": len(data.recipients),
        "message": "Certificate generation job created",
    }


@router.get("/jobs/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job.id,
        "event_name": job.event_name,
        "status": job.status,
        "total": job.total,
        "successful": job.successful,
        "failed": job.failed,
    }


@router.get("/jobs/{job_id}/certificates")
def get_job_certificates(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return [
        {
            "certificate_id": certificate.id,
            "recipient_name": certificate.recipient_name,
            "status": certificate.status,
            "error_message": certificate.error_message,
        }
        for certificate in job.certificates
    ]


@router.get("/certificates/{certificate_id}")
def download_certificate(
    certificate_id: int,
    db: Session = Depends(get_db),
):
    certificate = (
        db.query(Certificate)
        .filter(Certificate.id == certificate_id)
        .first()
    )

    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")

    if certificate.status != "completed" or not certificate.file_path:
        raise HTTPException(
            status_code=409,
            detail="Certificate is not ready for download",
        )

    file_path = Path(certificate.file_path)

    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Certificate file not found")

    return FileResponse(
        path=str(file_path),
        media_type="application/pdf",
        filename=file_path.name,
    )