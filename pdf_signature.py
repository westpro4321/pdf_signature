#!/usr/bin/env python

import os
from os import path
import sys
import csv
from fpdf import FPDF
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter


mainFile = sys.argv[1]
userText = sys.argv[2]
clientData = sys.argv[3]
outputDir = sys.argv[4]
x = float(sys.argv[5])
y = float(sys.argv[6])
pages = sys.argv[7]
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


class PDF(FPDF):
    row = []

    # needed to be overriden to print at the bottom of page
    def footer(self):
        self.set_font(font, size=fontSize)

        if y < 0 and self.row:
            self.set_y(y - (10 * (len(self.row) + 1)))
        else:
            self.set_y(y)

#        print 'X POS:',  self.get_x()
#        print 'Y POS:',  self.get_y()
        self.set_text_color(red, green, blue)
        self.set_x(x)

        self.cell(0, 10, txt=userText, ln=1, align='C')
        for item in self.row:
            self.cell(0, 10, txt=item, ln=1, align='C')

def printDoc(row = []):
    if not row:
        outName = os.path.join(outputDir, 'signed_' + path.basename(mainFile))
    else:
        outName = os.path.join(outputDir, '_'.join(row[0:2]) + '.pdf')

    print 'Out file', outName

    # Get our files ready
    input_file = PdfFileReader(open(mainFile, "rb"))
    page = input_file.getPage(0).mediaBox

    if page.getUpperRight_x() - page.getUpperLeft_x() > page.getUpperRight_y() - page.getLowerRight_y():
        orientation = 'L'
        size = (page.getUpperRight_y() - page.getLowerRight_y(), page.getUpperRight_x() - page.getUpperLeft_x())
    else:
        orientation = 'P'
        size = (page.getUpperRight_x() - page.getUpperLeft_x(), page.getUpperRight_y() - page.getLowerRight_y())

    width = page.getUpperRight_x() - page.getUpperLeft_x()

    print "orientation", orientation
    print "Size", size

    # generate watermark file
    pdf = PDF(orientation, 'in')
#    pdf = PDF(orientation, 'in', size)
    pdf.add_page()
    pdf.row = row
    pdf.output(outName)
    watermark = PdfFileReader(open(outName, "rb"))



    output_file = PdfFileWriter()

    print "Page size:", input_file.getPage(0).mediaBox

    # Number of pages in input document
    page_count = input_file.getNumPages()

    # Go through all the input file pages to add a watermark to them
    allPages = pages == "All"
    for page_number in range(page_count):
        input_page = input_file.getPage(page_number)
        if page_number == 0 or allPages:
            print "Watermarking page {} of {}".format(page_number, page_count)
            # merge the watermark with the page
            input_page.mergePage(watermark.getPage(0))
        # add page from input file to output document
        output_file.addPage(input_page)

    # finally, write "output" to document-output.pdf
    with open(outName, "wb") as outputStream:
        output_file.write(outputStream)

if not path.exists(clientData):
    printDoc()
else:
    with open(clientData) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            printDoc(row = row)



