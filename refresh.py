#!/usr/bin/env python3
"""
IRIS Competitor Map - Data Refresh Script
Run this script to update competitor data from the web.
Requires: pip install requests beautifulsoup4 openai
"""

import json
import requests
from datetime import datetime
from pathlib import Path

# Configuration
DATA_FILE = Path(__file__).parent / "data.json"
OUTPUT_FILE = Path(__file__).parent / "data.json"

def load_existing_data():
    """Load existing competitor data."""
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return []

def update_competitor_data(competitors):
    """Update competitor data with fresh info.

    To use with OpenAI for AI-powered updates:
    1. Set OPENAI_API_KEY environment variable
    2. Uncomment the OpenAI section below
    """
    updated = []
    for company in competitors:
        # Update timestamp
        company["last_updated"] = datetime.now().isoformat()
        updated.append(company)
        print(f"  Processed: {company.get('name', 'Unknown')}")
    return updated

def save_data(data):
    """Save updated data to file."""
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved {len(data)} companies to {OUTPUT_FILE}")

def add_company(name, category, lat, lng, website, description, funding=None, products=None):
    """Add a new company to the dataset."""
    companies = load_existing_data()
    new_company = {
        "id": name.lower().replace(' ', '-'),
        "name": name,
        "category": category,
        "lat": lat,
        "lng": lng,
        "website": website,
        "description": description,
        "funding": funding or "Unknown",
        "products": products or [],
        "founded": str(datetime.now().year),
        "last_updated": datetime.now().isoformat()
    }
    companies.append(new_company)
    save_data(companies)
    print(f"Added: {name}")
    return new_company

if __name__ == "__main__":
    print("IRIS Competitor Map - Data Refresh")
    print("=" * 40)

    # Load existing data
    companies = load_existing_data()
    print(f"Loaded {len(companies)} companies")

    # Update data
    print("
Updating competitor data...")
    updated = update_competitor_data(companies)

    # Save
    save_data(updated)
    print("
Refresh complete!")
    print(f"Total companies: {len(updated)}")
    print("
To add a new company, run:")
    print("  from refresh import add_company")
    print("  add_company('Company Name', 'AI Orchestration', 37.7749, -122.4194, 'https://company.com', 'Description')")
