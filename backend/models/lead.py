from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
import uuid

class Lead(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    phone: str
    email: Optional[str] = None
    area: str
    service: str
    budget: str
    message: Optional[str] = None
    source: str = "landing_page"
    status: str = "new"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Priya Sharma",
                "phone": "9876543210",
                "area": "Andheri West",
                "service": "Modular Kitchen",
                "budget": "₹3-7 Lakhs",
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
