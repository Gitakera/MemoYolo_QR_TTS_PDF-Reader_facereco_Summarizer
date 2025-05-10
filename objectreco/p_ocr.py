from paddleocr import PaddleOCR
import re
import numpy as np

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, use_gpu=True)

# Perform OCR on a cropped image
def paddle_ocr(cropped_image):
    result = ocr.ocr(cropped_image, det=False, rec=True, cls=False)
    text = ""
    for r in result:
        scores = r[0][1]
        if not np.isnan(scores) and scores > 0.6:  # Only process high scores
            text = r[0][0]

    # Clean text
    text = re.sub(r'\W', '', text).replace("O", "0")
    return text
