from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
import os
import sys
from reportlab.lib.units import inch

mainFile = sys.argv[1]
userText = sys.argv[2]
clientData = sys.argv[3]
outputDir = sys.argv[4]
x = float(sys.argv[5])
y = float(sys.argv[6])
pages = sys.argv[7]
allPages = pages == "All"
font = sys.argv[8]
fontSize = int(sys.argv[9])
color = int(sys.argv[10])
blue = color%256
green = (color/256)%256
red = ((color/256)/256)%256
width = 0.0

print 'Main pdf:', mainFile
print 'User text:', userText
print 'Client data:', clientData
print 'Output dir data:', outputDir
print 'X:', x
print 'Y:', y
print 'Pages:', pages
print 'Font:', font
print 'Font size:', fontSize
print 'R:', red
print 'G:', green
print 'B:', blue


#text = 'Company Name'# Folder in which PDF files will be watermarked. (Could be shared folder)
c = canvas.Canvas('watermark.pdf')
#c.setFontSize(fontSize)
c.setFillColorRGB(float(red)/256, float(green)/256, float(blue)/256)
c.setFont('Helvetica', fontSize)
c.drawString(x*inch, y*inch, userText)
c.save()

watermark = PdfFileReader(open("watermark.pdf", "rb"))
for file in [mainFile]:#os.listdir(folder_path):
    if file.endswith(".pdf"):
        output_file = PdfFileWriter()
        input_file = PdfFileReader(open(file, "rb"))
#        input_file = PdfFileReader(open(folder_path + '/'+ file, "rb"))
        page_count = input_file.getNumPages()
        for page_number in range(page_count):
            input_page = input_file.getPage(page_number)
            if page_number == 0 or allPages:
                input_page.mergePage(watermark.getPage(0))
            output_file.addPage(input_page)
        output_path = file.split('.pdf')[0] + '_watermarked' + '.pdf'
        with open(output_path, "wb") as outputStream:
            output_file.write(outputStream)
