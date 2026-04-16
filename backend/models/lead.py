from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Literal
from datetime import datetime
import uuid

# Status enum for quote tracking
QuoteStatus = Literal["submitted", "budget_discussion", "site_visit", "work_started"]

class StatusHistory(BaseModel):
    status: QuoteStatus
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    note: Optional[str] = None

class Lead(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    quote_number: str  # MA-YYYY-XXXXX format
    name: str
    phone: str
    email: Optional[str] = None
    area: str
    service: str
    budget: str
    message: Optional[str] = None
    source: str = "landing_page"
    status: QuoteStatus = "submitted"
    status_history: List[StatusHistory] = Field(default_factory=lambda: [StatusHistory(status="submitted")])
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "quote_number": "MA-2026-00001",
                "name": "Priya Sharma",
                "phone": "9876543210",
                "area": "Andheri West",
                "service": "Modular Kitchen",
                "budget": "₹3-7 Lakhs",
                "status": "submitted",
                "message": "Looking for a modern kitchen design"
            }
        }

class LeadCreate(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    area: str
    service: str
    budget: str
    message: Optional[str] = None

class StatusUpdate(BaseModel):
    status: QuoteStatus
    note: Optional[str] = None
