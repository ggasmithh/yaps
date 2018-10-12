import argparse
import os
import numpy
import scipy
import imageio

from scipy import ndimage
from tqdm import tqdm

import time

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
        data (imageio.core.util.Array) imageio image data
        width (int) width of image
        height (int) height of image

        luma (numpy.ndarray) numpy array of the same shape as self.data, but containing the equivalent luma values for each pixel
        sobel_coordinates (numpy.ndarray) numpy array of the same as self.data, but containing a 1-bit "sobelized" image of self.data as booleans
        segments (list) list of segments of pixel locations, as determined by the truth values in sobel_coordinates
    
    Private Attributes:
        none

    Arguments:
        data (obj) imageio image data
    """
    
    def __init__(self, data):
        self.data = data
        self.width, self.height, *rest = data.shape

       
        self.luma = self.__get_luma_values()
        self.sobel_coordinates = self.__get_sobel_coordinates()
        self.segments = self.__get_segments()

    def __get_luma_values(self):

        print("\nGenerating luma values. . .")

        luma = self.data.tolist()

        # this could totally be flattened into some sort of nested list comprehension
        for i in tqdm(range(0, len(luma))):
            for j in range(0, len(luma[i])):

                luma[i][j] = sum([x * y for x, y in zip(luma[i][j], [0.2126, 0.7152, 0.0722])])

                
        return numpy.asarray(luma)


    def __get_segments(self):

        temp_segments = []

        #start the first segment with the first pixel
        current_segment = [[0, 0]]

        print("\nGenerating segments. . .")
        for i in tqdm(range(0, self.width)):
            for j in range(0, self.height):

                #if the Pixel doesn't belong in this Segment, push the old one and start a new one
                #Segments are also confined to the column in which they started
                if (self.sobel_coordinates[current_segment[-1][0], current_segment[-1][1]] != self.sobel_coordinates[i, j]) or (current_segment[0][0] != i):
                    temp_segments.append(current_segment)
                    current_segment = [[i, j]]

                #otherwise, add this Pixel to the Segment
                else:
                    current_segment.append([i, j])

        return temp_segments

    def sort(self):
        """Iterates through the Image's Segments, sorts them if necessary,
            then stitches the newly sorted Segments together
        """

        temp_data = self.data

        print("\nSorting segments. . .")
        for segment in tqdm(self.segments):

            segment_start = segment[0]

            if not self.sobel_coordinates[segment_start[0], segment_start[1]]:
           
                luma_slice = self.luma[segment_start[0], segment_start[1]:segment_start[1] + len(segment)]

                segment = [x[1] for x in sorted(zip(luma_slice, segment))]

            for i in range(0, len(segment)):

                # this is the error that is currently driving me bonkers
                #    self.data[segment_start[0], segment_start[1] + i] = self.data[segment[i][0], segment[i][1]] 
                #      ValueError: could not broadcast input array from shape (2,3) into shape (3)

                temp_data[segment_start[0], segment_start[1] + i] = self.data[segment[i][0], segment[i][1]]

        self.data = temp_data

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

            start = time.time()

            input_image = Image(imageio.imread(INPUT))

            input_image.sort()

            end = time.time()

            print("Total elapsed time:", round(end - start, 3), "seconds.")

            input_image.save_to_disk(OUTPUT)

        
main()
