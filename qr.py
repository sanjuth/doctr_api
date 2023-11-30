from qrdet import QRDetector
import fitz
from PIL import Image
import cv2
from pyzbar.pyzbar import decode
import os
import numpy as np


class QRProcessor:
    def __init__(self):
        self.detector = QRDetector(model_size='s')

    def detect_qr_codes(self, image):
        try:
            detections = self.detector.detect(image=image, is_bgr=True)
            qr_code_data = []

            for detection in detections:
                x1, y1, x2, y2 = detection['bbox_xyxy']
                roi = image[int(y1)+1:int(y2)+1, int(x1)+1:int(x2)+1]
                decoded_objects = decode(roi)

                for obj in decoded_objects:
                    qr_code_data.append(obj.data.decode("utf-8"))

            return qr_code_data
        except Exception as e:
            print(f"Error detecting QR codes: {str(e)}")
            return []

    def process_image(self, path):
        try:
            image = cv2.imread(filename=path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            return self.detect_qr_codes(image)
        except Exception as e:
            print(f"Error processing image {path}: {str(e)}")
            return []

    def process_pdf(self, path, file_name):
        try:
            zoom = 2
            mat = fitz.Matrix(zoom, zoom)
            doc = fitz.open(path)
            qr_dict = {}

            for i, page in enumerate(doc):
                pix = page.get_pixmap(matrix=mat)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img_array = np.array(img)

                qr_codes = self.detect_qr_codes(img_array)
                qr_dict[f'{file_name} : {i}'] = qr_codes

            return qr_dict
        except Exception as e:
            print(f"Error processing PDF {file_name}: {str(e)}")
            return {}

    def process_file(self, path, file_name):
        if file_name.lower().endswith(".pdf"):
            return self.process_pdf(path, file_name)
        else:
            return {file_name: self.process_image(path)}
        
        
