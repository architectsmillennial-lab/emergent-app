from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
import sys

# Import models and services
sys.path.append(str(Path(__file__).parent))
from models.lead import Lead, LeadCreate
from services.email_service import EmailService


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize email service after loading env
email_service = EmailService()

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")  # Ignore MongoDB's _id field
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello from Millenial Architects API"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    # Convert to dict and serialize datetime to ISO string for MongoDB
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    # Exclude MongoDB's _id field from the query results
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    
    return status_checks

# Lead Management Routes
@api_router.post("/leads", response_model=Lead)
async def create_lead(lead_input: LeadCreate):
    """
    Create a new lead from quote form submission
    Sends email notifications to business and customer
    """
    try:
        # Create lead object
        lead_data = lead_input.model_dump()
        lead = Lead(**lead_data)
        
        # Save to database
        doc = lead.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        await db.leads.insert_one(doc)
        
        # Send email notifications
        try:
            # Send notification to business owner
            email_service.send_lead_notification(lead_data)
            logger.info(f"Lead notification sent for: {lead.name}")
        except Exception as e:
            logger.error(f"Failed to send business notification: {str(e)}")
            # Don't fail the request if email fails
        
        try:
            # Send confirmation to customer (if email provided)
            if lead_data.get('email'):
                email_service.send_customer_confirmation(lead_data)
                logger.info(f"Customer confirmation sent to: {lead_data.get('email')}")
        except Exception as e:
            logger.error(f"Failed to send customer confirmation: {str(e)}")
            # Don't fail the request if email fails
        
        return lead
    except Exception as e:
        logger.error(f"Error creating lead: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create lead: {str(e)}")

@api_router.get("/leads", response_model=List[Lead])
async def get_leads(limit: int = 100, status: Optional[str] = None):
    """Get all leads, optionally filtered by status"""
    try:
        query = {}
        if status:
            query["status"] = status
            
        leads = await db.leads.find(query, {"_id": 0}).sort("created_at", -1).limit(limit).to_list(limit)
        
        # Convert ISO string timestamps back to datetime objects
        for lead in leads:
            if isinstance(lead.get('created_at'), str):
                lead['created_at'] = datetime.fromisoformat(lead['created_at'])
        
        return leads
    except Exception as e:
        logger.error(f"Error fetching leads: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch leads: {str(e)}")

@api_router.get("/leads/{lead_id}", response_model=Lead)
async def get_lead(lead_id: str):
    """Get a specific lead by ID"""
    try:
        lead = await db.leads.find_one({"id": lead_id}, {"_id": 0})
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        if isinstance(lead.get('created_at'), str):
            lead['created_at'] = datetime.fromisoformat(lead['created_at'])
        
        return Lead(**lead)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching lead: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch lead: {str(e)}")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()