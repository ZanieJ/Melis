import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

try:
    from ocr_service import process_pdf
except Exception as e:
    print(f"❌ Failed to import OCR service: {e}")
    process_pdf = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    if process_pdf is None:
        return {"status": "error", "reason": "OCR service failed to import"}

    results = []
    for file in files:
        try:
            content = await file.read()
            file_results = await process_pdf(file.filename, content)
            results.extend(file_results)
        except Exception as e:
            print(f"❌ Error processing file {file.filename}: {e}")
            results.append({"error": str(e), "file": file.filename})
    return {"status": "success", "data": results}