import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from tempfile import NamedTemporaryFile

from ocr import OCRModule
from qr import QRProcessor  # Assuming you have a QR module with the QRProcessor class

app = FastAPI(
    title="doctr api",
    description="api for document recognition",
    version="0.0.1",
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ocr_module = OCRModule()
qr_processor = QRProcessor()

@app.get('/notify/v1/health')
def get_health():
    return {"msg": "OK"}

@app.post("/ocr")
async def doctr_ocr(file: UploadFile = File(...)):
    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file.file.read())
        temp_file.seek(0)

        file_name = file.filename
        file_path = temp_file.name

    try:
        # OCR Processing
        ocr_response, output_filepath = ocr_module.process_document(file_path, file_name)
        with open(output_filepath, 'r') as file_content:
            text_response = file_content.read()

        # QR Code Processing
        qr_response = qr_processor.process_file(file_path, file_name)

        return {
            "ocr_response": ocr_response,
            "text_response": text_response,
            "qr_response": qr_response
        }
    except Exception as e:
        return {
            "error": "Something went wrong",
            "error_detail": str(e)
        }

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level="info")
