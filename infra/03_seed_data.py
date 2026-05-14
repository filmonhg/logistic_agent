"""Seed mock logistics data into DynamoDB."""
import os
import uuid
import boto3
from decimal import Decimal

REGION = os.environ.get("AWS_REGION", "us-west-2")
TABLE = os.environ.get("DDB_TABLE", "LogisticsOffers")

dynamodb = boto3.resource("dynamodb", region_name=REGION)
table = dynamodb.Table(TABLE)

OFFERS = [
    {"origin": "Mombasa",       "destination": "Kigali",    "shipper": "EastAfrica Logistics", "rate_usd": 2400, "transit_days": 7},
    {"origin": "Mombasa",       "destination": "Kampala",   "shipper": "Swift Cargo",          "rate_usd": 1800, "transit_days": 5},
    {"origin": "Mombasa",       "destination": "Kigali",    "shipper": "Rift Valley Movers",   "rate_usd": 2200, "transit_days": 8},
    {"origin": "Dar es Salaam", "destination": "Kigali",    "shipper": "Tanga Trans",          "rate_usd": 2600, "transit_days": 9},
    {"origin": "Nairobi",       "destination": "Kigali",    "shipper": "EastAfrica Logistics", "rate_usd": 1900, "transit_days": 4},
    {"origin": "Mombasa",       "destination": "Bujumbura", "shipper": "Lake Express",         "rate_usd": 2800, "transit_days": 10},
    {"origin": "Mombasa",       "destination": "Goma",      "shipper": "Congo Routes Ltd",     "rate_usd": 3100, "transit_days": 11},
    {"origin": "Nairobi",       "destination": "Kampala",   "shipper": "Swift Cargo",          "rate_usd": 1500, "transit_days": 3},
]

print(f"→ Seeding {len(OFFERS)} offers into {TABLE}...")
with table.batch_writer() as batch:
    for o in OFFERS:
        item = dict(o)
        item["offer_id"] = str(uuid.uuid4())
        item["rate_usd"] = Decimal(str(item["rate_usd"]))
        item["transit_days"] = Decimal(str(item["transit_days"]))
        batch.put_item(Item=item)
        print(f"  + {o['origin']:<14} → {o['destination']:<10}  ${o['rate_usd']:<5}  ({o['shipper']})")

print("\n✓ Seeded successfully.")
