import os
import tempfile
import time
import httpx
import re
from pdf2image import convert_from_bytes
from supabase_client import insert_pallet_record

OCR_API_KEY = os.getenv("OCR_SPACE_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

async def process_pdf(filename: str, content: bytes):
    images = convert_from_bytes(content, dpi=300)
    results = []

    for i, image in enumerate(images):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_img:
            image.save(temp_img.name)
            ocr_text = await ocr_image(temp_img.name)
            os.unlink(temp_img.name)

        pallet_ids = re.findall(r"\b\d{18}\b", ocr_text)
        page_number = i + 1

        for pallet_id in pallet_ids:
            record = {
                "pallet_id": pallet_id,
                "document_name": filename,,
                "page_number": page_number,
            }
            await insert_pallet_record(record)
            results.append(record)

        time.sleep(1)  # 1-second delay to stay within OCR.Space free limits

    return results

async def ocr_image(image_path: str) -> str:
    url = "https://api.ocr.space/parse/image"
    with open(image_path, "rb") as f:
        files = {"file": f}
        data = {
            "apikey": OCR_API_KEY,
            "OCREngine": 2,
            "language": "eng",
        }
        async with httpx.AsyncClient() as client:
            r = await client.post(url, data=data, files=files)
            result = r.json()
            if result.get("IsErroredOnProcessing"):
                return ""
            return result.get("ParsedResults", [{}])[0].get("ParsedText", "")
