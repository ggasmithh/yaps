from PIL import Image
from sys import argv
import os
import random

IMG_FORMATS = ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.gif', '.bmp']

#Read image
if os.path.isfile(argv[1]):
    if os.path.splitext(argv[1])[1].lower() in IMG_FORMATS:
        im = Image.open(argv[1])

im_width, im_height = im.size


#Splitting the image into its respective bands, i.e. Red, Green,
#and Blue for RGB
r,g,b = im.split()

#list to hold our bands when they're sorted
new_bands = []

for band in [r, g, b]:

    #convert the band into a bytearray
    band_list = list(band.tobytes())

    #convert the list of all the pixels into lists of pixel in each row
    rows = []
    for i in range(0, len(band_list), im_width):
        rows.append(band_list[i:i + im_width])

    #sort each row
    for each in rows:
        each.sort()

    #put our list of rows back into one big ole' list
    new_band_list = []
    for each in rows:
        for element in each:
            new_band_list.append(element)

    #put our bytearray back into a bytes object
    band_bytes = bytes(new_band_list)

    #recreate the band from the mode of the original band, our bytes object,
    #and the size of the original image
    band = Image.frombytes(band.mode, im.size, band_bytes)

    #add our newly sorted band to the list of sorted bands
    new_bands.append(band)


#put the sorted bands of the picture back together. . . 
im_new = Image.merge("RGB", tuple(new_bands))

# . . . save the image. . . 
im_new.save("output.png")

#. . and show the image
im_new.show()


pause = input("Hit enter to close. . . ")