from fastapi import FastAPI, UploadFile, File
from typing import List
from ocr_service import process_pdf

app = FastAPI()

@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    all_results = []
    for file in files:
        content = await file.read()
        results = await process_pdf(file.filename, content)
        all_results.extend(results)
    return {"status": "success", "results": all_results}
