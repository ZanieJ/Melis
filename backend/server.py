from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ocr_service import process_pdf

app = FastAPI()

# Enable CORS for all origins (for GitHub Pages access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your GitHub Pages URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    print(f"📄 Received: {file.filename}")
    
    # Run your OCR logic
    results = await process_pdf(file.filename, content)

    print(f"✅ OCR processed {file.filename}, found {len(results)} entries.")
    return {"status": "success", "data": results}
