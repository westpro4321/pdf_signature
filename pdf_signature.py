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
position = float(sys.argv[5])
align = sys.argv[6]
pages = sys.argv[7]
font = sys.argv[8]
fontSize = int(sys.argv[9])

print 'Main pdf:', mainFile
print 'User text:', userText
print 'Client data:', clientData
print 'Output dir data:', outputDir
print 'Position:', position
print 'Align:', align
print 'Pages:', pages
print 'Font:', font
print 'Font size:', fontSize


class PDF(FPDF):
    row = []

    # needed to be overriden to print at the bottom of page
    def footer(self):
        self.set_font(font, size=fontSize)

        if position < 0 and self.row:
            self.set_y(position - (10 * (len(self.row) + 1)))
        else:
            self.set_y(position)
        print 'Y POS:',  self.get_y()

        self.cell(0, 10, txt=userText, ln=1, align=align[0])
        for item in self.row:
            self.cell(0, 10, txt=item, ln=1, align=align[0])

def printDoc(row = []):
    if not row:
        outName = os.path.join(outputDir, 'signed_' + path.basename(mainFile))
    else:
        outName = os.path.join(outputDir, '_'.join(row[0:2]) + '.pdf')

    print 'Out file', outName


    # generate watermark file
    pdf = PDF()
    pdf.add_page()
    pdf.row = row
    pdf.output(outName)
    watermark = PdfFileReader(open(outName, "rb"))

    # Get our files ready
    input_file = PdfFileReader(open(mainFile, "rb"))
    output_file = PdfFileWriter()

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



