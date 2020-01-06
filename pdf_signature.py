#!/usr/bin/env python

import os
import sys
import csv
from fpdf import FPDF
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

mainFile = sys.argv[1]
clientData = sys.argv[2]
outputDir = sys.argv[3]
print 'Main pdf:', mainFile
print 'Client data:', clientData
print 'Output dir data:', outputDir

dataList = []
with open(clientData) as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        outName = os.path.join(outputDir, '_'.join(row[0:2]) + '.pdf')
        # generate watermark file
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=24)
        pdf.cell(200, 10, txt="Ta kopia zostala utworzona dla:", ln=1, align="C")

        for item in row:
            pdf.cell(200, 10, txt=item, ln=1, align="C")

        outName = os.path.join(outputDir, '_'.join(row[0:2]) + '.pdf')
        pdf.output(outName)

        watermark = PdfFileReader(open(outName, "rb"))

        # Get our files ready
        input_file = PdfFileReader(open(mainFile, "rb"))
        output_file = PdfFileWriter()

        # Number of pages in input document
        page_count = input_file.getNumPages()

        # Go through all the input file pages to add a watermark to them
        for page_number in range(page_count):
            input_page = input_file.getPage(page_number)
            if page_number == 0:
                print "Watermarking page {} of {}".format(page_number, page_count)
                # merge the watermark with the page
                input_page.mergePage(watermark.getPage(0))
            # add page from input file to output document
            output_file.addPage(input_page)

        # finally, write "output" to document-output.pdf
        with open(outName, "wb") as outputStream:
            output_file.write(outputStream)
