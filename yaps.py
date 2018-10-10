import argparse
import os
import numpy
import scipy
import imageio

from scipy import ndimage
from tqdm import tqdm

IMG_FORMATS = ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.gif', '.bmp']

parser = argparse.ArgumentParser(description="pixel sort an image or video")
parser.add_argument("input", help = "input file (must be an image)")
INPUT = parser.parse_args().input

#os.path.split() splits the full path into everything before the last "/" of the
#filepath, and everything after it (i.e. the filename). split(".") splits the
#filename into everything before the period (the name itself) and everything
#after the period (the extension)
OUTPUT = os.path.split(INPUT)[1].split(".")[0] + "_output"

class Pixel:
    """Stores the information of one pixel

    Public Attributes:
        x (int) x location of Pixel (measured by pixels from the left)
        y (int) y location of Pixel (measured by pixels from the top)
        luma (int) luma value of Pixel
        is_sobel (bool) whether the pixel is part of a Sobel edge
    
    Private Attributes:
        none

    Arguments:
        x (int) x location of Pixel
        y (int) y location of Pixel
        rgb (list) Red, Green, and Blue values of Pixel
        is_sobel (bool) whether the pixel is part of a Sobel edge

    Notes:
        See following link for more on Luma values:
            #https://en.wikipedia.org/wiki/Luma_(video)
    """

    def __init__(self, x, y, rgb, is_sobel):
        self.x = x
        self.y = y
        self.rgb = rgb
        self.luma = rgb[0] * 0.2126 + rgb[1] * 0.7152 + rgb[2] * 0.0722
        self.is_sobel = is_sobel

class Segment:
    """Stores of one "segment" of the image

    Public Attributes:
        start_x (int) x location beginning of Segment (measured by pixels from the left)
        start_y (int) y location beginning of Segment (measured by pixels from the top)
        length (int) length of the Segment
        is_sobel (bool) whether the segment is part of a Sobel edge
    
    Private Attributes:
        __pixel_list (list) a list of the Pixels in the Segment

    Arguments:
        first_pixel (Pixel) the first Pixel of the segment (can't have a 0 Pixel segment)

    Notes:
        See following link for more on Luma values:
            #https://en.wikipedia.org/wiki/Luma_(video)
    """

    def __init__(self, first_pixel):
        self.start_x = first_pixel.x
        self.start_y = first_pixel.y

        self.is_sobel = first_pixel.is_sobel

        self.__pixel_list = [first_pixel]

    def add_pixel(self, pixel):
        self.__pixel_list.append(pixel)

    def get_length(self):
        return len(self.__pixel_list)

    def sort(self):
        self.__pixel_list.sort(key=lambda pixel:pixel.luma)

    def get_pixels(self):
        return [pixel.rgb for pixel in self.__pixel_list]

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

        self.sobel_coordinates = self.__get_sobel_coordinates()
        self.segments = self.__get_segments()


    def __get_segments(self):

        print("\nPutting pixels into objects. . . ")
        temp_pixels = [ Pixel(i, j, self.data[i, j], self.sobel_coordinates[i, j])
                        for i in tqdm(range(0, self.width))
                        for j in range(0, self.height) ]

        temp_segments = []
 
        ## organize pixels into segments

        #start the first segment with the first pixel
        current_segment = Segment(temp_pixels[0])

        print("\nPutting pixels into segments. . .")
        for pixel in tqdm(temp_pixels):
            #if the Pixel doesn't belong in this Segment, push the old one and start a new one
            #Segments are also confined to the column in which they started
            if (current_segment.is_sobel != pixel.is_sobel) or (current_segment.start_x != pixel.x):
                temp_segments.append(current_segment)
                current_segment = Segment(pixel)

            #otherwise, add this Pixel to the Segment
            else:
                current_segment.add_pixel(pixel)

        return temp_segments

    def sort(self):
        """Iterates through the Image's Segments, sorts them if necessary, t
            then stitches the newly sorted Segments together
        """

        print("\nSorting segments. . .")
        for segment in tqdm(self.segments):
            if not segment.is_sobel:
                segment.sort()

            pixels = segment.get_pixels()
            for i in range(0, len(pixels) - 1):
                self.data[segment.start_x, segment.start_y + i] = pixels[i]

            #self.data[segment.start_x, (segment.start_y - 1:segment.start_y + segment.get_length())] = segment.get_pixels()

    def __get_sobel_coordinates(self):

        print("\nGetting sobel coordinates")

        temp_image = self.data.astype('int32')

        dx = ndimage.sobel(temp_image, 0) #horizontal derivative
        dy = ndimage.sobel(temp_image, 1) #vertical image

        mag = numpy.hypot(dx, dy) #magnitude

        mag *= 255 / numpy.max(mag) #normalize

        coordinates = numpy.zeros((self.width, self.height), dtype=numpy.bool)
    
        for i in tqdm(range(0, self.width)):
            for j in range(0, self.height):
                if numpy.any(mag[i, j] > 128):
                    coordinates[i, j] = True

        coordinates[(i, j)]

        return coordinates

    def save_to_disk(self, name):
        """Saves Image object to disk as png file, with no regard for the 
            user's input file format

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
