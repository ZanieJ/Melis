from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ocr_service import process_pdf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/test-upload")  # 🔥 MUST MATCH your frontend
async def upload_file(file: UploadFile = File(...)):
    print(f"📥 Received test file: {file.filename}")
    content = await file.read()
    results = await process_pdf(file.filename, content)
    return {"status": "success", "data": results}
