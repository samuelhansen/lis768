import sys
import pytesseract
from wand.image import Image
from PIL import Image as PI
import os
import io

helpString = "ocr.py -- ocr a directory of pdfs with tesseract!\nUseage: ./ocr.py  [Path to PDF Directory] [Path to Output Directory]"

path=os.path.dirname(os.path.abspath(__file__))


ocrPath = path + '/ocredTexts/'
toOcrPath = path + '/filesToTranscribe/'

# check for invalid or help options
if len(sys.argv)>1:
    if len(sys.argv) > 3:
        print("invalid options")
        print(helpString)
        quit()

    if sys.argv[1] == "-h" or sys.argv[1] == "help":
        print(helpString)
        quit()

    if len(sys.argv) >= 2:
        if sys.argv[1].endswith('/'):
            toOcrPath = sys.argv[1]
        else:
            toOcrPath = sys.argv[1] + '/'

    if len(sys.argv) == 3:
        if sys.argv[2].endswith('/'):
            ocrPath = sys.argv[2]
        else:
            ocrPath = sys.argv[2] + '/'



if not os.path.exists(ocrPath):
    os.makedirs(ocrPath)

pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'


for fName in sorted(os.listdir(toOcrPath)):
    if fName.endswith('.pdf'):
        req_image = []
        final_text = []
        noExtFName=os.path.splitext(fName)[0]
        pdfPath=toOcrPath + fName
        image_pdf = Image(filename=pdfPath, resolution=300)
        image_jpeg = image_pdf.convert('jpeg')

        for img in image_jpeg.sequence:
            img_page = Image(image=img)
            req_image.append(img_page.make_blob('jpeg'))


        for img in req_image:
            txt = pytesseract.image_to_string(PI.open(io.BytesIO(img)))
            final_text.append(txt)
        ocrText=ocrPath + noExtFName + '.txt'
        with open(ocrText, 'a') as file:
            for x in final_text:
                file.write(x + '\n')


print(ocrPath + ' ' + toOcrPath)