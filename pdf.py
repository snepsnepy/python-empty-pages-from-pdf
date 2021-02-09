from PyPDF2 import PdfFileWriter, PdfFileReader
from pathlib import Path
import os
import fitz
import img2pdf
import shutil
import pathlib
import sys
import datetime
import uuid
from PIL import Image
from pdf2image import convert_from_path

now = datetime.datetime.today()
nTime = now.strftime("%d-%m-%Y")
fnameTime = now.strftime("%Y-%m-%d_%H-%M-%S")

src = 'Input'

dest = 'Output_' + \
    fnameTime
blankDest = 'Blanks_' + \
    fnameTime

files = Path().cwd().glob(dest + "/**/*.pdf")
blankFiles = Path().cwd().glob(blankDest + "/**/*.pdf")

outputDel = Path().cwd().glob(dest + "/**/*.png")
outputPdf = Path().cwd().glob(dest + "/**/*.pdf")

pageNum = 0
p = 0

if(os.path.isdir(dest)) == False:
    destination = shutil.copytree(src, dest)

try:
    for filename in files:
        pages_to_keep = []
        base = os.path.basename(filename)
        doc = fitz.open(filename)

        for page in doc:
            colorCount = 0
            # number of page
            page = doc.loadPage(pageNum)
            pix = page.getPixmap()

            # Take the path of the parent directory of each file
            path = os.path.dirname(filename)
            # Convert the path to string
            stringFolderPath = str(path)
            baseStr = str(os.path.splitext(base)[0])
            # print("BASE STR: ", baseStr)
            start = 'pag_'
            end = '_'
            output = stringFolderPath + "\%spag_%s_.png" % (baseStr, p)
            pix.writePNG(output)
            p += 1
            pageNum += 1

            imagePath = Path(output).absolute()
            image = Image.open(imagePath).convert("L")  # Convert the image
            im1 = Image.Image.getcolors(image)
            for img in im1:
                colorCount += 1
            if(colorCount > 150):
                os.remove(imagePath)
                baseImage = os.path.basename(imagePath)
                pageToKeep = int(baseImage.split(start)[1].split(end)[0])
                pages_to_keep.append(pageToKeep)

        fname = str(filename)
        infile = PdfFileReader(fname, 'rb')
        output = PdfFileWriter()

        for i in pages_to_keep:
            print
            p = infile.getPage(i)
            output.addPage(p)

            with open(fname, "wb") as f:
                output.write(f)

        print("Done with ---> ", fname)

        p = 0
        pageNum = 0

    if(os.path.isdir(blankDest)) == False:
        destination = shutil.copytree(dest, blankDest)

    for pdfFile in blankFiles:
        os.remove(pdfFile)

    for pngfile in outputDel:
        os.remove(pngfile)

    input("-----> Press Enter To Exit <-----")

except:
    print(sys.exc_info()[0], "occurred.")
    input("Press Enter To Exit.")
