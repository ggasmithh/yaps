import argparse
import os
import numpy
import scipy
import imageio
import time

from scipy import ndimage

IMG_FORMATS = ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.gif', '.bmp']

parser = argparse.ArgumentParser(description="pixel sort an image")
parser.add_argument("input", help = "input file (must be an image)")
INPUT = parser.parse_args().input

#os.path.split() splits the full path into everything before the last "/" of the
#filepath, and everything after it (i.e. the filename). split(".") splits the
#filename into everything before the period (the name itself) and everything
#after the period (the extension)
OUTPUT = os.path.split(INPUT)[1].split(".")[0] + "_output"
"""
    luma (numpy.ndarray) numpy array of the same shape as self.data, but containing the equivalent luma values for each pixel
    sobel_coordinates (numpy.ndarray) numpy array of the same as self.data, but containing a 1-bit "sobelized" image of self.data as booleans
    segments (list) list of segments of pixel locations, as determined by the truth values in sobel_coordinates

"""

def __init__(self, data):

    
    self.luma = self.__get_luma_values()
    self.sobel_coordinates = self.__get_sobel_coordinates()
    self.segments = self.__get_segments()

def get_luma_values(image_data):

    print("\nGenerating luma values. . .")

    luma = image_data.tolist()

    # this could totally be flattened into some sort of nested list comprehension
    for i in range(0, len(luma)):
        for j in range(0, len(luma[i])):

            luma[i][j] = sum([x * y for x, y in zip(luma[i][j], [0.2126, 0.7152, 0.0722])])

            
    return numpy.asarray(luma)

def get_sobel_coordinates(image_data, width, height):

    print("\nGetting sobel coordinates")

    temp_image_data = image_data.astype('int32')

    dx = ndimage.sobel(temp_image_data, 0) #horizontal derivative
    dy = ndimage.sobel(temp_image_data, 1) #vertical image

    mag = numpy.hypot(dx, dy) #magnitude

    mag *= 255 / numpy.max(mag) #normalize

    coordinates = numpy.zeros((width, height), dtype=numpy.bool)

    for i in range(0, width):
        for j in range(0, height):
            if numpy.any(mag[i, j] > 128):
                coordinates[i, j] = True

    return coordinates

def get_segments(sobel_coordinates, width, height):

    temp_segments = []

    #start the first segment with the first pixel
    current_segment = [[0, 0]]

    print("\nGenerating segments. . .")
    for i in range(0, width):
        for j in range(0, height):

            #if the Pixel doesn't belong in this Segment, push the old one and start a new one
            #Segments are also confined to the column in which they started
            if (sobel_coordinates[current_segment[-1][0], current_segment[-1][1]] != sobel_coordinates[i, j]) or (current_segment[0][0] != i):
                temp_segments.append(current_segment)
                current_segment = [[i, j]]

            #otherwise, add this Pixel to the Segment
            else:
                current_segment.append([i, j])

    return temp_segments

def sort(image_data, luma, sobel_coordinates, segments):
    """Iterates through the Image's Segments, sorts them if necessary,
        then stitches the newly sorted Segments together
    """

    temp_image_data = image_data

    print("\nSorting segments. . .")
    for segment in segments:

        segment_start = segment[0]

        if not sobel_coordinates[segment_start[0], segment_start[1]]:
        
            luma_slice = luma[segment_start[0], segment_start[1]:segment_start[1] + len(segment)]

            segment = [x[1] for x in sorted(zip(luma_slice, segment))]

        for i in range(0, len(segment)):

            # this is the error that is currently driving me bonkers
            #    self.data[segment_start[0], segment_start[1] + i] = self.data[segment[i][0], segment[i][1]] 
            #      ValueError: could not broadcast input array from shape (2,3) into shape (3)

            temp_image_data[segment_start[0], segment_start[1] + i] = image_data[segment[i][0], segment[i][1]]

    return temp_image_data


def save_to_disk(image_data, name):
    """Saves Image object to disk as png file, with no regard for the 
        user's input file format

        Arguments:
            name (str) desired name of output file, sans extension
    """

    imageio.imwrite("{}.png".format(name), image_data)

def main():
    if os.path.isfile(INPUT):
        file_extension = os.path.splitext(INPUT)[1].lower()
        if file_extension in IMG_FORMATS:

            image_data = imageio.imread(INPUT)
            image_width, image_height, *rest = image_data.shape

            start_time = time.time() # I only care about measuring performance of this chunk.

            luma_values = get_luma_values(image_data)
            sobel_coordinates = get_sobel_coordinates(image_data, image_width, image_height)
            segments = get_segments(sobel_coordinates, image_width, image_height)

            output_image_data = sort(image_data, luma_values, sobel_coordinates, segments)

            print("--- %s seconds ---" % (time.time() - start_time))
        
            save_to_disk(output_image_data, OUTPUT)

        
main()
