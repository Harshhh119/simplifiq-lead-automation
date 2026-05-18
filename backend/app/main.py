from fastapi import FastAPI, BackgroundTasks, status
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import LeadInput, LeadResponse
from app.services.enricher import generate_company_insights
from app.services.pdf_gen import create_audit_pdf
from app.services.mailer import send_report_email
from app.services.google_api import log_lead_to_sheets, archive_pdf_to_drive
import uuid
import os

app = FastAPI(title="SimplifIQ Ingestion Engine")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

async def processing_pipeline(lead_id: str, lead: LeadInput):
    pdf_filename = f"report_{lead_id}.pdf"
    pdf_path = os.path.join("/tmp", pdf_filename) if os.name != 'nt' else pdf_filename
    current_status = "Failed"
    try:
        insights = await generate_company_insights(lead.company_name, lead.company_website or "")
        create_audit_pdf(lead.company_name, insights, pdf_path)
        await archive_pdf_to_drive(pdf_path, lead.company_name)
        await send_report_email(lead.email, lead.name, lead.company_name, pdf_path)
        current_status = "Success"
    except Exception as e:
        current_status = f"Failed: {str(e)}"
    finally:
        await log_lead_to_sheets(lead.name, lead.email, lead.company_name, current_status)
        if os.path.exists(pdf_path):
            try: os.remove(pdf_path)
            except Exception: pass

@app.post("/api/v1/leads", response_model=LeadResponse, status_code=status.HTTP_202_ACCEPTED)
async def submit_lead(lead: LeadInput, background_tasks: BackgroundTasks):
    lead_tracking_id = str(uuid.uuid4())
    background_tasks.add_task(processing_pipeline, lead_tracking_id, lead)
    return LeadResponse(
        status="Accepted",
        message="Lead received. Generating report and emailing it shortly.",
        lead_id=lead_tracking_id
    )