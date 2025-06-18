import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_TABLE = "NDAs"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def insert_pallet_record(record):
    supabase.table(SUPABASE_TABLE).insert(record).execute()
