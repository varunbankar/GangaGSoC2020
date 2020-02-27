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

# PDF File splitter according to pages
def pdfSplitter(path):
    
    # Strip .pdf
    filename = os.path.splitext(os.path.basename(path))[0]

    pdf = PdfFileReader(path)

    # Split PDF
    for page in range(pdf.getNumPages()):

        # Write individual page into another PDF
        pdfWriter = PdfFileWriter()
        pdfWriter.addPage(pdf.getPage(page))
        outputFilename = f"{filename}_PAGE{page+1}.pdf"
        with open(os.path.join(currentDir, outputFilename), "wb") as out:
            pdfWriter.write(out)

        print(f"Created: {outputFilename}")

#--------------------------------------#

if __name__ == "__main__":
    path = "CERN.pdf"
    pdfSplitter(path)

########################################