# OCR Backend with OCR.Space and Supabase

## 🚀 What it does

- Accepts multiple PDF uploads
- Splits PDFs into per-page images
- Sends each page to OCR.Space API (with 1-second delay between calls)
- Extracts 18-digit pallet IDs
- Saves: pallet_id, document_name, page_number → Supabase

## 📦 Requirements

- Free OCR.Space API key (used in `.env`)
- Supabase project with `NDAs` table
- Deployed on Render (Free Tier OK)

## 🛠 Deploy

1. Add your `.env` file (copy from `.env.example`)
2. Deploy on Render with Docker
3. POST PDFs to `/upload` endpoint

## 🔐 Environment Variables

```
SUPABASE_URL=...
SUPABASE_ANON_KEY=...
OCR_SPACE_API_KEY=...
```

## 🧪 Endpoint

```
POST /upload
Content-Type: multipart/form-data
Body: file=[PDFs...]
```
