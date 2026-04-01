#!/usr/bin/env python3
"""
Millenial Architects - Lead Management Tool
View, export, and manage your leads from the command line
"""

import requests
import json
from datetime import datetime, timedelta
import sys

BACKEND_URL = "https://interior-quote-hub.preview.emergentagent.com"

def get_all_leads():
    """Fetch all leads from the database"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/leads")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching leads: {e}")
        return []

def display_leads_summary(leads):
    """Display a summary of all leads"""
    print("\n" + "="*80)
    print(f"📊 MILLENIAL ARCHITECTS - LEADS SUMMARY")
    print("="*80 + "\n")
    
    print(f"Total Leads: {len(leads)}")
    
    # Count by service
    services = {}
    budgets = {}
    areas = {}
    
    for lead in leads:
        service = lead.get('service', 'Unknown')
        budget = lead.get('budget', 'Unknown')
        area = lead.get('area', 'Unknown')
        
        services[service] = services.get(service, 0) + 1
        budgets[budget] = budgets.get(budget, 0) + 1
        areas[area] = areas.get(area, 0) + 1
    
    print("\n📋 By Service:")
    for service, count in sorted(services.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {service}: {count}")
    
    print("\n💰 By Budget:")
    for budget, count in sorted(budgets.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {budget}: {count}")
    
    print("\n📍 By Area:")
    for area, count in sorted(areas.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {area}: {count}")
    
    print("\n" + "="*80 + "\n")

def display_leads_detailed(leads, limit=None):
    """Display detailed information for each lead"""
    print("\n" + "="*80)
    print(f"📝 DETAILED LEADS REPORT")
    print("="*80 + "\n")
    
    leads_to_show = leads[:limit] if limit else leads
    
    for i, lead in enumerate(leads_to_show, 1):
        print(f"Lead #{i}")
        print(f"  Name: {lead['name']}")
        print(f"  Phone: +91 {lead['phone']}")
        print(f"  Email: {lead.get('email', 'Not provided')}")
        print(f"  Area: {lead['area']}")
        print(f"  Service: {lead['service']}")
        print(f"  Budget: {lead['budget']}")
        print(f"  Status: {lead['status']}")
        
        if lead.get('message'):
            print(f"  Message: {lead['message']}")
        
        created = lead['created_at']
        print(f"  Submitted: {created}")
        print("-" * 80)
    
    if limit and len(leads) > limit:
        print(f"\n... and {len(leads) - limit} more leads")
    
    print()

def export_to_csv(leads, filename="leads_export.csv"):
    """Export leads to CSV file"""
    import csv
    
    if not leads:
        print("No leads to export")
        return
    
    fieldnames = ['name', 'phone', 'email', 'area', 'service', 'budget', 'message', 'status', 'created_at']
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for lead in leads:
            row = {k: lead.get(k, '') for k in fieldnames}
            writer.writerow(row)
    
    print(f"✅ Exported {len(leads)} leads to {filename}")

def get_today_leads(leads):
    """Filter leads from today"""
    today = datetime.now().date()
    today_leads = []
    
    for lead in leads:
        created = datetime.fromisoformat(lead['created_at'].replace('Z', '+00:00'))
        if created.date() == today:
            today_leads.append(lead)
    
    return today_leads

def get_this_week_leads(leads):
    """Filter leads from this week"""
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    week_leads = []
    
    for lead in leads:
        created = datetime.fromisoformat(lead['created_at'].replace('Z', '+00:00'))
        if created >= week_ago:
            week_leads.append(lead)
    
    return week_leads

def main():
    """Main menu"""
    print("\n🏠 Millenial Architects - Lead Management")
    print("=" * 50)
    print("1. View Summary")
    print("2. View All Leads (Detailed)")
    print("3. View Today's Leads")
    print("4. View This Week's Leads")
    print("5. Export All Leads to CSV")
    print("6. Export Today's Leads to CSV")
    print("0. Exit")
    print("=" * 50)
    
    choice = input("\nEnter your choice: ").strip()
    
    leads = get_all_leads()
    
    if not leads:
        print("No leads found in database")
        return
    
    if choice == '1':
        display_leads_summary(leads)
    elif choice == '2':
        display_leads_detailed(leads)
    elif choice == '3':
        today_leads = get_today_leads(leads)
        print(f"\n📅 Today's Leads: {len(today_leads)}")
        display_leads_detailed(today_leads)
    elif choice == '4':
        week_leads = get_this_week_leads(leads)
        print(f"\n📅 This Week's Leads: {len(week_leads)}")
        display_leads_detailed(week_leads)
    elif choice == '5':
        filename = f"leads_all_{datetime.now().strftime('%Y%m%d')}.csv"
        export_to_csv(leads, filename)
    elif choice == '6':
        today_leads = get_today_leads(leads)
        filename = f"leads_today_{datetime.now().strftime('%Y%m%d')}.csv"
        export_to_csv(today_leads, filename)
    elif choice == '0':
        print("Goodbye!")
        sys.exit(0)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
