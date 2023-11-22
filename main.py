import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from tempfile import NamedTemporaryFile
from ocr import OCR_function

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


@app.get('/notify/v1/health')
def get_health():
    return dict(msg='OK')


@app.post("/ocr")
async def doctr_ocr(file: UploadFile = File(...)):

    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file.file.read())
        temp_file.seek(0)

        file_name = file.filename
        file_path = temp_file.name

    try:
        response, output_filepath = OCR_function(file_path,file_name)
        with open(output_filepath, 'r') as file:
            file_content = file.read()
        
        return{
            "json_response": response,
            "text_response": file_content
        }
    except:
        return{
            "error":"something went wrong"
        }


if __name__=='__main__':
    uvicorn.run('main:app',host='0.0.0.0',port=8000,log_level="info")