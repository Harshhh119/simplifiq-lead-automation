# SimplifIQ Lead Ingestion & Automation Engine

An end-to-end backend prototype built with FastAPI designed to automate lead intake, perform AI-driven contextual web enrichment, generate professional PDF audit briefs via ReportLab, and handle asynchronous email dispatch.

---

##  System Architecture & Workflow
* **Lead Ingestion Endpoint:** A validated FastAPI POST route (`/api/v1/leads`) accepts incoming payload data.
* **Asynchronous Processing:** Leverages FastAPI's `BackgroundTasks` to instantly release the request-response thread, returning a `202 Accepted` status.
* **Web Scraping:** Pulls contextual text data from target corporate websites using an asynchronous HTTP client.
* **Gemini AI Enrichment:** Passes scraped data to Google's **Gemini 1.5 Flash** API via the `v1beta` REST framework using structured JSON payload schemas to extract domain values, bottlenecks, and core insights.
* **PDF Report Compilation:** A specialized ReportLab layout module constructs a styled, padded executive briefing document.
* **Email Outreach Dispatch:** Connects over an SMTP mail client to drop the final PDF attachment straight into the evaluator's inbox.

---

##  Technology Stack
* **Core Framework:** FastAPI (Python 3.11+)
* **ASGI Server:** Uvicorn (with hot-reload infrastructure)
* **Data Validation:** Pydantic v2
* **Generative AI:** Google Gemini REST API (`v1beta` integration framework)
* **Asynchronous HTTP Client:** HTTPX
* **Document Compilation:** ReportLab PDF Engine
* **Secret Management:** Python-Dotenv

---

##  Local Setup & Installation
1. **Clone the Repository:** `git clone https://github.com/YOUR_GITHUB_USERNAME/simplifiq-lead-automation.git`
   `cd simplifiq-lead-automation`
2. **Configure the Virtual Environment:** `cd backend`
   `python -m venv .venv`
   `.\.venv\Scripts\Activate.ps1` *(On Windows PowerShell)*
3. **Install Dependencies:** `pip install -r requirements.txt`
4. **Setup Environment Variables (`.env`):** Create a `.env` file inside the `backend/` folder and paste your matching credentials:
   `GEMINI_API_KEY=AIzaSy...your_actual_key...`
   `SMTP_USER=harshchaudhary5593@gmail.com`
   `SMTP_PASSWORD=xxxx_xxxx_xxxx_xxxx` *(Your 16-character Google App Password)*
   `GOOGLE_SHEET_ID=not_created`
   `GOOGLE_DRIVE_FOLDER_ID=not_created`
5. **Setup Credentials File:** Create a empty JSON block inside a file named `service_account.json` within your `backend/` directory to pass internal validation modules: `{}`

---

##  Execution & Testing Instructions
1. Boot up your local development server from your terminal window:
   `python -m uvicorn app.main:app --reload`
2. Open your web browser and navigate directly to your interactive API dashboard:
    **http://127.0.0.1:8000/docs**
3. Open the `POST /api/v1/leads` route container, click **"Try it out"**, and paste this clean sandbox test payload to safely clear external domain firewall blocks:
   `{ "name": "Harsh Vardhan", "email": "harshchaudhary5593@gmail.com", "company_name": "Scraping Sandbox", "company_website": "https://toscrape.com/" }`
4. Click **"Execute"**. Your API will instantly return a `202 Accepted` network status, and your compiled briefing document will land in your `harshchaudhary5593@gmail.com` inbox within 10-15 seconds.

---

##  Security & Resilience Design
* **Credential Protection:** The project's root `.gitignore` parameters strictly block your custom `.env` file, local `.venv/` binaries, and placeholder `service_account.json` datasets from accidentally leaking onto public GitHub trackers.
* **Error Handlers:** System layout fallbacks are hardcoded into the data pipeline to ensure that if a corporate target domain enforces anti-scraping firewalls, the background pipeline gracefully appends pre-structured fallback analysis insights so the PDF generation and email transmission threads complete without fracturing the loop.
