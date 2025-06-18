# Melissa OCR Backend

This backend accepts PDF files, extracts 18-digit pallet IDs from each page using OCR.Space, and uploads the results to a Supabase table.

## ✅ Features

- Upload multiple PDFs
- Process every page of each PDF
- Convert pages to PNG
- Send each page to OCR.Space
- Extract 18-digit pallet IDs from OCR text
- Insert pallet ID + document name + page number into Supabase

## 📄 Output Format

Each record inserted into the `NDAs` table will look like:

- `pallet_id`: 18-digit number
- `document_name`: e.g. `yourfile_pg3.pdf`
- `page_number`: page number from the PDF

## 🚀 Deployment (Render)

### Docker-Based Deploy Steps

1. Connect your GitHub repo containing this code
2. Create a new **Web Service**
3. Choose **"Docker"** environment
4. Set these Environment Variables:

```
OCR_SPACE_API_KEY=your_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key
```

Render will build your image and run:

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

You're done!
