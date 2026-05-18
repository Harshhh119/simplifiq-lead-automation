from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class LeadInput(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    company_name: str = Field(..., min_length=2)
    company_website: Optional[str] = None

class LeadResponse(BaseModel):
    status: str
    message: str
    lead_id: str