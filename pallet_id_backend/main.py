from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from supabase import create_client, Client
import os

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
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
    data = [r.dict() for r in records]
    try:
        response = supabase.table("pallet_records").insert(data).execute()
        return {"status": "success", "inserted": len(data)}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
