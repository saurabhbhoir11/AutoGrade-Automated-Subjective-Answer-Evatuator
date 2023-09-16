from google.cloud import vision
import os 

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client_file_vision_api.json"

client = vision.ImageAnnotatorClient()

with open('test.jpg', 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

response = client.text_detection(image=image)
texts = response.text_annotations

for text in texts:
    print(text.description)
