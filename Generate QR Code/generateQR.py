import qrcode
import qrcode.image.svg
import os
import inspect, os.path
import pyperclip
from datetime import datetime

import sys

def make_qrpng():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    src = input("""\n[Encode or Paste (CTRL+V)]
    Input text/source for QR: """) # http://rssocar.psa.gov.ph/benguet

    qr.add_data(src)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    filepath = os.path.dirname(os.path.realpath(__file__)) # get working directory
    filename = "QRCode_PNG_{}.png".format(datetime.utcnow().strftime('%Y%m%d%H%M%S%f')) # rename the file with extension
    pathwfile = "{}\{}".format(filepath, filename) # combine working directory and filename with file extension
    result = pathwfile.replace('\\', '\\\\') # replace single slash to double slash for file generation path

    img.save(result)

    print("\nFILE SAVED AS: {}".format(filename))
    print("\nFILE SAVED TO: {}".format(filepath))
    print("""\n***Directory to file copied to clipboard.***
    ***Open File Explorer and Paste (CTRL+V) the path.***""")
    pyperclip.copy("{}".format(filepath))
    pyperclip.paste()

    # openpathfolder = "{}\\".format(filepath) # get only working
    # result2 = openpathfolder.replace('\\', "//") # replace single slash to double slash for file generation path
    # open(result2)


def make_qrsvg():

    src = input("""[Encode or Paste (CTRL+V)]
    Input text/source for QR: """) # http://rssocar.psa.gov.ph/benguet

    factory = qrcode.image.svg.SvgPathImage

    img = qrcode.make(src, image_factory=factory)

    filepath = os.path.dirname(os.path.realpath(__file__)) # get working directory
    filename = "QRCode_SVG_{}.svg".format(datetime.utcnow().strftime('%Y%m%d%H%M%S%f')) # rename the file with extension
    pathwfile = "{}\{}".format(filepath, filename) # combine working directory and filename with file extension
    result = pathwfile.replace('\\', '\\\\') # replace single slash to double slash for file generation path

    img.save(result)

    print("\nFILE SAVED AS: {}".format(filename))
    print("\nFILE SAVED TO: {}".format(filepath))
    print("""\n***Directory to file copied to clipboard.***
    ***Open File Explorer and Paste (CTRL+V) the path.***""")
    pyperclip.copy("{}".format(filepath))
    pyperclip.paste()

    # openpathfolder = "{}\\".format(filepath) # get only working
    # result2 = openpathfolder.replace('\\', "//") # replace single slash to double slash for file generation path
    # open(result2)

choice = str(input("""\n
=============================INFO===============================
Developed with https://pypi.org/project/qrcode/
Converted with https://github.com/brentvollebregt/auto-py-to-exe
Compiled by https://github.com/zenpao
=============================INFO===============================

Choose an option: 
        P - .PNG-file type QR Code (Common)
        V - .SVG-file type QR Code
        X - Exit
Choice: """))
if choice.lower() == 'p':
    make_qrpng()
    print("\nQR GENERATED: Please verify the QR Code by scanning.")
    input("\nPress ENTER key to exit..")
elif choice.lower() == 'v':
    make_qrsvg()
    print("\nQR GENERATED: Please verify the QR Code by scanning.")
    input("\nPress ENTER key to exit..")
elif choice.lower() == 'x':
    quit()
else:
    print("\nINVALID INPUT!")