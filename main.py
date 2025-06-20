from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from supabase import create_client, Client
import os
import uvicorn

app = FastAPI()

# Environment Variables (set in Render dashboard)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")  # Use the service role key

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class PalletRecord(BaseModel):
    pallet_id: str
    pdf_name: str
    page_number: int

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/upload_pallets")
async def upload_pallets(records: List[PalletRecord]):
    # Convert to Supabase-compatible format
    data = [{
        "pallet_id": r.pallet_id,
        "pdf_name": r.pdf_name,
        "page_number": r.page_number
    } for r in records]

    try:
        response = supabase.table("pallet_records").insert(data).execute()
        return {"status": "success", "inserted": len(data)}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
