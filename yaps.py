import argparse
import os
import numpy
import imageio

IMG_FORMATS = ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.gif', '.bmp']

parser = argparse.ArgumentParser(description="pixel sort an image or video")
parser.add_argument("input", help = "input file (must be an image)")
INPUT = parser.parse_args().input

#os.path.split() splits the full path into everything before the last "/" of the
#filepath, and everything after it (i.e. the filename). split(".") splits the
#filename into everything before the period (the name itself) and everything
#after the period (the extension)
OUTPUT = os.path.split(INPUT)[1].split(".")[0] + "_output"


class Image:
    """Stores imageio image data, and the image's attributes.

    Public Attributes:
        data (obj) imageio image data
        width (int) width of image
        height (int) height of image
    
    Private Attributes:
        none

    Arguments:
        data (obj) imageio image data
    """
    
    def __init__(self, data):
        self.data = data
        self.width, self.height, *rest = data.shape

    def sort(self):
        """Sorts the Image's data by the greatest R, G, or B value
        """
        temp_data = self.data.tolist()

        for row in temp_data:
            row.sort(key=lambda x:max(x))

        self.data = numpy.asarray(temp_data)

    def save_to_disk(self, name):
        """Saves Image object to disk as png file.

            Arguments:
                name (str) desired name of output file, sans extension
        """
        imageio.imwrite("{}.png".format(name), self.data)

def main():
    if os.path.isfile(INPUT):
        file_extension = os.path.splitext(INPUT)[1].lower()
        if file_extension in IMG_FORMATS:
            input_image = Image(imageio.imread(INPUT))
            input_image.sort()
            input_image.save_to_disk(OUTPUT)

main()
