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
from models.lead import Lead, LeadCreate, StatusUpdate, StatusHistory
from services.email_service import EmailService
from utils.quote_utils import generate_quote_number, get_status_display_info, get_all_statuses


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
    Generates unique quote number and sends email notifications
    """
    try:
        # Generate unique quote number
        quote_number = await generate_quote_number(db)
        
        # Create lead object
        lead_data = lead_input.model_dump()
        lead_data['quote_number'] = quote_number
        lead = Lead(**lead_data)
        
        # Save to database
        doc = lead.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        # Convert status_history to dict
        doc['status_history'] = [h.model_dump() for h in lead.status_history]
        for h in doc['status_history']:
            h['timestamp'] = h['timestamp'].isoformat()
        
        await db.leads.insert_one(doc)
        
        # Send email notifications
        try:
            # Send notification to business owner
            email_service.send_lead_notification({**lead_data, 'quote_number': quote_number})
            logger.info(f"Lead notification sent for: {lead.name} ({quote_number})")
        except Exception as e:
            logger.error(f"Failed to send business notification: {str(e)}")
        
        try:
            # Send confirmation to customer (if email provided)
            if lead_data.get('email'):
                email_service.send_customer_confirmation({**lead_data, 'quote_number': quote_number})
                logger.info(f"Customer confirmation sent to: {lead_data.get('email')}")
        except Exception as e:
            logger.error(f"Failed to send customer confirmation: {str(e)}")
        
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

@api_router.get("/leads/report/summary")
async def get_leads_summary():
    """Get a summary report of all leads"""
    try:
        leads = await db.leads.find({}, {"_id": 0}).to_list(1000)
        
        total = len(leads)
        by_service = {}
        by_budget = {}
        by_area = {}
        by_status = {}
        
        for lead in leads:
            service = lead.get('service', 'Unknown')
            budget = lead.get('budget', 'Unknown')
            area = lead.get('area', 'Unknown')
            status = lead.get('status', 'new')
            
            by_service[service] = by_service.get(service, 0) + 1
            by_budget[budget] = by_budget.get(budget, 0) + 1
            by_area[area] = by_area.get(area, 0) + 1
            by_status[status] = by_status.get(status, 0) + 1
        
        return {
            "total_leads": total,
            "by_service": by_service,
            "by_budget": by_budget,
            "by_area": by_area,
            "by_status": by_status,
            "latest_leads": leads[:5] if leads else []
        }
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate summary: {str(e)}")

@api_router.get("/leads/track/{quote_number}")
async def track_quote(quote_number: str):
    """
    Track a quote by its quote number
    Public endpoint for customers to check their quote status
    """
    try:
        lead = await db.leads.find_one({"quote_number": quote_number.upper()}, {"_id": 0})
        
        if not lead:
            raise HTTPException(status_code=404, detail="Quote not found")
        
        # Convert ISO strings back to datetime for response
        if isinstance(lead.get('created_at'), str):
            lead['created_at'] = datetime.fromisoformat(lead['created_at'])
        
        if 'status_history' in lead:
            for h in lead['status_history']:
                if isinstance(h.get('timestamp'), str):
                    h['timestamp'] = datetime.fromisoformat(h['timestamp'])
        
        # Add status display info
        all_statuses = get_all_statuses()
        current_status_index = all_statuses.index(lead['status'])
        
        timeline = []
        for i, status in enumerate(all_statuses):
            status_info = get_status_display_info(status)
            
            # Check if this status is in history
            history_item = next((h for h in lead.get('status_history', []) if h['status'] == status), None)
            
            timeline.append({
                "status": status,
                "label": status_info['label'],
                "icon": status_info['icon'],
                "description": status_info['description'],
                "completed": i <= current_status_index,
                "current": i == current_status_index,
                "timestamp": history_item['timestamp'] if history_item else None,
                "note": history_item.get('note') if history_item else None
            })
        
        return {
            "quote_number": lead['quote_number'],
            "name": lead['name'],
            "service": lead['service'],
            "area": lead['area'],
            "budget": lead['budget'],
            "current_status": lead['status'],
            "created_at": lead['created_at'],
            "timeline": timeline
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error tracking quote: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to track quote: {str(e)}")

@api_router.patch("/leads/{quote_id}/status")
async def update_lead_status(quote_id: str, status_update: StatusUpdate):
    """
    Update the status of a lead
    For admin use - requires authentication in production
    """
    try:
        # Find the lead
        lead = await db.leads.find_one(
            {"$or": [{"id": quote_id}, {"quote_number": quote_id.upper()}]},
            {"_id": 0}
        )
        
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        # Create new status history entry
        new_history = StatusHistory(
            status=status_update.status,
            note=status_update.note
        )
        
        # Update the lead
        update_doc = {
            "status": status_update.status,
            "$push": {
                "status_history": {
                    "status": status_update.status,
                    "timestamp": new_history.timestamp.isoformat(),
                    "note": status_update.note
                }
            }
        }
        
        result = await db.leads.update_one(
            {"$or": [{"id": quote_id}, {"quote_number": quote_id.upper()}]},
            update_doc
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="Failed to update status")
        
        logger.info(f"Status updated for {lead.get('quote_number', quote_id)}: {status_update.status}")
        
        return {
            "success": True,
            "quote_number": lead.get('quote_number'),
            "new_status": status_update.status,
            "message": f"Status updated to {status_update.status}"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update status: {str(e)}")

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