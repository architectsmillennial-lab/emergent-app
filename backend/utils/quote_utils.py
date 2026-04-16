"""
Quote number generator and utilities
"""
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase

async def generate_quote_number(db: AsyncIOMotorDatabase) -> str:
    """
    Generate unique quote number in format MA-YYYY-XXXXX
    MA = Millenial Architects
    YYYY = Current year
    XXXXX = Sequential number (padded to 5 digits)
    """
    current_year = datetime.now().year
    
    # Get the count of leads created this year
    year_start = datetime(current_year, 1, 1)
    count = await db.leads.count_documents({
        "created_at": {"$gte": year_start.isoformat()}
    })
    
    # Increment for next quote number
    next_number = count + 1
    
    # Format: MA-2026-00142
    quote_number = f"MA-{current_year}-{next_number:05d}"
    
    return quote_number

def get_status_display_info(status: str) -> dict:
    """Get display information for each status"""
    status_info = {
        "submitted": {
            "label": "Quote Submitted",
            "icon": "✅",
            "description": "We've received your quote request"
        },
        "budget_discussion": {
            "label": "Budget Discussion",
            "icon": "💬",
            "description": "Our team is reviewing your requirements"
        },
        "site_visit": {
            "label": "Site Visit Scheduled",
            "icon": "🏠",
            "description": "Visit scheduled to assess your space"
        },
        "work_started": {
            "label": "Work Started",
            "icon": "🔨",
            "description": "Your project is underway!"
        }
    }
    return status_info.get(status, {})

def get_all_statuses() -> list:
    """Get ordered list of all statuses"""
    return ["submitted", "budget_discussion", "site_visit", "work_started"]
