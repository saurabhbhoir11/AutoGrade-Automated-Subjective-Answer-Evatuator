import cv2
import numpy as np

def preprocess(image):
    # Preprocessing
    image = cv2.imdecode(np.frombuffer(image, np.uint8), -1)
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    norm_img = gray_img / 255.0  # Normalize to 0-1 range
    norm_img = cv2.normalize(norm_img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

    # Denoising
    denoised_img_nlm = cv2.fastNlMeansDenoising(norm_img, None, 8, 31, 7)  # Adjust parameters as needed
    denoised_img_final = cv2.bilateralFilter(denoised_img_nlm, 100, 75, 75)  # Further denoising with bilateral filter
    # cv2.imshow("Denoised Image", denoised_img_final)
    # cv2.waitKey(0)

    _, output = cv2.imencode('.png', denoised_img_final)

    return output
