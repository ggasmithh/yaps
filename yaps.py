#TODO: MAKE AN OPTION TO MAKE A TIMELAPSE OF THE IMAGE BEING SORTED.
#AFTER EACH ROW IS SORTED, SAVE A FRAME, AT THE END USE FFMPEG TO CREATE
#A VIDEO

import argparse
import os
import random
import shutil

from PIL import Image

IMG_FORMATS = ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.gif', '.bmp']
VID_FORMATS = ['.mp4']

parser = argparse.ArgumentParser(description="pixel sort an image or video")
parser.add_argument("input", help = "input file (must be image or .mp4 video)")
INPUT = parser.parse_args().input

#os.path.split() splits the full path into everything before the last "/" of the
#filepath, and everything after it (i.e. the filename). split(".") splits the
#filename into everything before the period (the name itself) and everything
#after the period (the extension)
OUTPUT = os.path.split(INPUT)[1].split(".")[0] + "_output"

def image_handler(image):

    print("---PIXEL SORTING IMAGE---")
    image_new = sort_image(image)
    image_new.save("{}.png".format(OUTPUT))
    print("Done!")


def create_temp_folders(input_path, output_path):
    #make some temporary folders
    if not os.path.exists(input_path):
        os.makedirs(input_path)
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)


def video_to_frames(input_path, video):
    #convert the given video to a set of frames, store them in a temp input directory
    print("Converting video to frames. . .", end = "")
    os.system("ffmpeg -i {} -r 30 {}frame_%05d.jpeg >> /dev/null 2>&1".format(input_path, video))
    print("Done!")


def frames_to_video():
    print("Converting sorted frames to video. . . ", end = "")
    #convert the images from the temporary output directory to a video
    os.system("ffmpeg -framerate 30 -i {}frame_%05d.jpeg {}.mp4 \
    >> /dev/null 2>&1".format(output_path, OUTPUT))
    print("Done!")


def clean_temp():
    print("Cleaning up. . . ", end = "")
    #finally, delete our temporary folders
    shutil.rmtree(input_path)
    shutil.rmtree(output_path)


def video_handler(video, input_path, output_path):

    print("---PIXEL SORTING VIDEO---")

    create_temp_folders()
    video_to_frames(video)

    print("Sorting frames. . . ")

    #I'm going to be using these values potentially thousands of times. It looks
    #hella amateur but it's better this way.
    file_list = os.listdir(input_path)
    num_files = len(file_list)
    i = 0

    for file in file_list:
        
        current_progress = int((i / num_files) * 100)

        #update progress every 5%
        if current_progress % 5 == 0:
            print(str(current_progress) + '% complete', end="\r")
            
        #open the jpeg of the frame, sort it, and store it as sorted_frame
        sorted_frame = sort_image(Image.open(input_path + file))

        #save the sorted frame to a temporary output directory
        sorted_frame.save(output_path + file)

        i += 1

    print("Done!")

    frames_to_video()


#Accepts an unsorted Image object, returns a sorted Image object
def sort_image(im):

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

    return im_new


def main():
    #Read image or video
    if os.path.isfile(INPUT):

        file_extension = os.path.splitext(INPUT)[1].lower()
        if file_extension in IMG_FORMATS:
            image_handler(Image.open(INPUT))

        elif file_extension in VID_FORMATS:
            video_handler(INPUT, "temp/input/", "temp/output/")

main()
