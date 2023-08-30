import pdf2image
import pytesseract

def pdf_to_text(pdf_file):
  """Extracts text from a PDF file using Tesseract.

  Args:
    pdf_file: The path to the PDF file to convert.

  Returns:
    The text extracted from the PDF file.
  """

  images = pdf2image.convert_from_path(pdf_file)
  text = ''
  for image in images:
    text += pytesseract.image_to_string(image)

  return text

if __name__ == '__main__':
  pdf_file = 'my_pdf.pdf'
  text = pdf_to_text(pdf_file)
  print(text)