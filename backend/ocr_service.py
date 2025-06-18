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

# ✅ Print environment variables (partial for security)
print("🔧 OCR_API_KEY:", OCR_API_KEY[:5] if OCR_API_KEY else "None")
print("🔧 SUPABASE_URL:", SUPABASE_URL or "None")
print("🔧 SUPABASE_KEY:", SUPABASE_KEY[:5] if SUPABASE_KEY else "None")

async def process_pdf(filename: str, content: bytes):
    print(f"📄 Starting PDF processing: {filename}")
    images = convert_from_bytes(content, dpi=300)
    results = []

    for i, image in enumerate(images):
        page_number = i + 1
        print(f"🖼️ Converting page {page_number} to image...")

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_img:
            image.save(temp_img.name)
            print(f"📤 OCR processing image: {temp_img.name}")
            ocr_text = await ocr_image(temp_img.name)
            os.unlink(temp_img.name)

        print(f"🔍 Extracted text: {ocr_text[:100]}...")  # Preview first 100 characters

        pallet_ids = re.findall(r"\b\d{18}\b", ocr_text)
        print(f"📦 Found pallet IDs on page {page_number}: {pallet_ids}")

        for pallet_id in pallet_ids:
            record = {
                "pallet_id": pallet_id,
                "document_name": filename,
                "page_number": page_number,
            }
            print(f"📝 Inserting record into Supabase: {record}")
            await insert_pallet_record(record)
            results.append(record)

        time.sleep(1)  # 1-second delay to stay within OCR.Space free limits

    print(f"✅ Finished processing {filename}")
    return results

async def ocr_image(image_path: str) -> str:
    print("📤 Sending OCR request with key:", OCR_API_KEY[:5] if OCR_API_KEY else "None")
    url = "https://api.ocr.space/parse/image"

    with open(image_path, "rb") as f:
        files = {"file": f}
        data = {
            "apikey": OCR_API_KEY,
            "OCREngine": 2,
            "language": "eng",
        }

        async with httpx.AsyncClient() as client:
            try:
                r = await client.post(url, data=data, files=files)
                result = r.json()
                print("📥 OCR response:", result)
                if result.get("IsErroredOnProcessing"):
                    print("❌ OCR API errored on processing")
                    return ""
                return result.get("ParsedResults", [{}])[0].get("ParsedText", "")
            except Exception as e:
                print("❌ OCR request failed:", e)
                return ""
