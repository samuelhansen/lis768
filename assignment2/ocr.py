import pytesseract
from wand.image import Image
from PIL import Image as PI
import os
import io

path=os.path.dirname(os.path.abspath(__file__))

path +='/1927-0013-Wall.pdf'
# # path='asdf.txt'
# #
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
req_image = []
final_text = []

image_pdf = Image(filename=path, resolution=600)
image_jpeg = image_pdf.convert('jpeg')

for img in image_jpeg.sequence:
    img_page = Image(image=img)
    req_image.append(img_page.make_blob('jpeg'))


for img in req_image:
    txt = pytesseract.image_to_string(PI.open(io.BytesIO(img)))
    final_text.append(txt)

with open('ocrPDF.txt', 'a') as file:
    for x in final_text:
        file.write(x + '\n')



#now lets convert the PDF to Image
    #this is good resolution As far as I know
# with Image(filename=path, resolution=200) as img:
#     #keep good quality
#     img.compression_quality = 80
#     #save it to tmp name
#     img.save(filename="temp/temp%s.jpg" % uuid_set)


