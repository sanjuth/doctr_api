# ocr_module.py
import os
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

class OCRModule:
    def __init__(self):
        self.model = ocr_predictor(pretrained=True)

    def process_document(self, file_path, file_name):
        try:
            if file_name.lower().endswith(".pdf"):
                document = DocumentFile.from_pdf(file_path)
            else:
                document = DocumentFile.from_images(file_path)

            result = self.model(document)
            json_response = result.export()
            output_file_path = 'output.txt'

            self._write_output_file(json_response, output_file_path)
            return json_response, output_file_path

        except Exception as e:
            error_log = f"Error processing {file_name}: {str(e)}"
            print(error_log)
            raise e

    def _write_output_file(self, json_response, output_file_path):
        with open(output_file_path, "w") as text_file:
            for page in json_response['pages']:
                for block in page['blocks']:
                    for line in block['lines']:
                        for word in line['words']:
                            text_file.write(word['value'] + " ")
                        text_file.write("\n")
                    text_file.write("\n")
                text_file.write("\n")
