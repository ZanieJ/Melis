# ocr_service/main.py
from fastapi import FastAPI, UploadFile, File
from paddleocr import PaddleOCR
import shutil
import uuid

app = FastAPI()

@app.post("/ocr")
async def run_ocr(file: UploadFile = File(...)):
    temp_path = f"/tmp/{uuid.uuid4()}.png"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    result = ocr.ocr(temp_path, cls=True)
    return {"text": result}
