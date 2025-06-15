FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    swig \
    wget \
    libgl1-mesa-glx \
    libglib2.0-0 \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
    && pip install --use-pep517 --no-build-isolation -r requirements.txt

# Pre-download PaddleOCR models
RUN mkdir -p /root/.paddleocr/whl/det/en/en_PP-OCRv3_det_infer && \
    wget -q -O /root/.paddleocr/whl/det/en/en_PP-OCRv3_det_infer/en_PP-OCRv3_det_infer.tar \
      https://paddleocr.bj.bcebos.com/PP-OCRv3/english/en_PP-OCRv3_det_infer.tar && \
    tar -xf /root/.paddleocr/whl/det/en/en_PP-OCRv3_det_infer/en_PP-OCRv3_det_infer.tar -C /root/.paddleocr/whl/det/en/en_PP-OCRv3_det_infer

RUN mkdir -p /root/.paddleocr/whl/rec/en/en_PP-OCRv3_rec_infer && \
    wget -q -O /root/.paddleocr/whl/rec/en/en_PP-OCRv3_rec_infer/en_PP-OCRv3_rec_infer.tar \
      https://paddleocr.bj.bcebos.com/PP-OCRv3/english/en_PP-OCRv3_rec_infer.tar && \
    tar -xf /root/.paddleocr/whl/rec/en/en_PP-OCRv3_rec_infer/en_PP-OCRv3_rec_infer.tar -C /root/.paddleocr/whl/rec/en/en_PP-OCRv3_rec_infer

RUN mkdir -p /root/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer && \
    wget -q -O /root/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer/ch_ppocr_mobile_v2.0_cls_infer.tar \
      https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar && \
    tar -xf /root/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer/ch_ppocr_mobile_v2.0_cls_infer.tar -C /root/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer

# Copy backend code
COPY backend/ .

# Healthcheck for container
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget --spider -q http://localhost:10000/health || exit 1

# Expose FastAPI port
EXPOSE 10000

# Start FastAPI server
CMD ["python", "main.py"]

