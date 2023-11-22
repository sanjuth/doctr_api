import os

from doctr.io import DocumentFile
from doctr.models import ocr_predictor

model = ocr_predictor(pretrained=True)


def OCR_function(file_path, file_name):
    is_pdf = False
    try:
        if (file_name[-3:] == "pdf"):
            document = DocumentFile.from_pdf(file_path)
            is_pdf = True
        else:
            document = DocumentFile.from_images(file_path)
        result = model(document)
        json_response = result.export()

        # output_file_path = os.path.join(file_name + '_output.txt')
        output_file_path = os.path.join('output.txt')

        pages = json_response['pages']
        with open(output_file_path, "w") as text_file:
            for p in pages:
                for i in p['blocks']:
                    for j in i['lines']:
                        for k in j['words']:
                            text_file.write(k['value']+" ")
                        text_file.write("\n")
                    text_file.write("\n")
                text_file.write("\n")
        
        return json_response, output_file_path

    except Exception as e:
        error_log = f"Error processing {file_name}: {str(e)}"
        print(error_log)
        raise e
