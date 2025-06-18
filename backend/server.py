from fastapi import FastAPI, UploadFile, File
from ocr_service import process_pdf
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    results = []
    for file in files:
        content = await file.read()
        file_results = await process_pdf(file.filename, content)
        results.extend(file_results)
    return {"status": "success", "data": results}
