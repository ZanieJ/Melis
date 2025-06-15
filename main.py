from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
import tempfile
from supabase import create_client, Client

from paddleocr import PaddleOCR  # Keep import at top but delay initialization

app = FastAPI()

# --- CORS setup ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Supabase configuration ---
SUPABASE_URL = "https://cassouhzovotgdhzssqg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Health Endpoints ---
@app.get("/")
def root():
    return {"message": "Service is live 🎉"}

@app.get("/health")
def health():
    return {"status": "ok"}

# --- OCR Endpoint (lazy-loaded OCR) ---
@app.post("/extract")
async def extract(files: list[UploadFile] = File(...)):
    # Lazy-load OCR inside the request handler to reduce RAM on cold start
    ocr = PaddleOCR(
        use_angle_cls=False,  # reduce RAM usage
        lang='en',
        det_model_dir='/root/.paddleocr/whl/det/en/en_PP-OCRv3_det_infer',
        rec_model_dir='/root/.paddleocr/whl/rec/en/en_PP-OCRv3_rec_infer',
        cls_model_dir='/root/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer'
    )

    for file in files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            doc = fitz.open(tmp.name)
            for page_number, page in enumerate(doc, start=1):
                pix = page.get_pixmap()
                img_path = tmp.name + f"_page_{page_number}.png"
                pix.save(img_path)
                result = ocr.ocr(img_path, cls=False)  # angle classification disabled
                for line in result[0]:
                    text = line[1][0]
                    if "pallet" in text.lower():
                        supabase.table("NDAs").insert({
                            "pallet_id": text,
                            "document_name": file.filename,
                            "page_number": page_number
                        }).execute()
    return {"status": "completed"}

# --- Pallet Search Endpoint ---
@app.post("/search")
async def search(data: dict):
    pallet_ids = data.get("pallet_ids", [])
    results = []
    for pid in pallet_ids:
        query = supabase.table("NDAs").select("*").eq("pallet_id", pid).execute()
        results.extend(query.data)
    return results
