########################################
####### GANGA CHALLENGE PART 1-2 #######
######### PDF SPLITTER MODULE ##########
########################################

# Imports
import os
from PyPDF2 import PdfFileReader, PdfFileWriter

#--------------------------------------#

# Current Directory
currentDir = os.path.dirname(os.path.realpath(__file__))

def pdfSplitter(path):
    """ Split PDF into individual pages """
    
    # Strip .pdf
    filename = os.path.splitext(os.path.basename(path))[0]

    pdf = PdfFileReader(path)

    # Split PDF
    for page in range(pdf.getNumPages()):

        # Write individual page into another PDF
        pdfWriter = PdfFileWriter()
        pdfWriter.addPage(pdf.getPage(page))
        outputFilename = "{}_PAGE{}.pdf".format(filename, (int(page)+1))
        with open(os.path.join(currentDir, outputFilename), "wb") as out:
            pdfWriter.write(out)

        print("Created: {}".format(outputFilename))

#--------------------------------------#

if __name__ == "__main__":
    path = "CERN.pdf"
    pdfSplitter(path)

########################################