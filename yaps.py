import os
import random
import shutil
from sys import argv

from PIL import Image


IMG_FORMATS = ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.gif', '.bmp']
VID_FORMATS = ['.mp4']


def image_handler(image):

    image_new = sort_image(image)
    image_new.save("output.png")


def video_handler(video):

    print("---PIXEL SORTING VIDEO---")

    #make some temporary folders
    if not os.path.exists("temp/input"):
        os.makedirs("temp/input")
    
    if not os.path.exists("temp/output"):
        os.makedirs("temp/output")

    #convert the given video to a set of frames, store them in a temp input directory
    print("Converting video to frames. . .", end = "")
    os.system("ffmpeg -i {} -r 30 temp/input/frame_%05d.jpeg >> /dev/null 2>&1".format(video))
    print("Done!")

    print("Sorting frames. . . ")

    #I'm going to be using these values potentially thousands of times. It looks
    #hella amateur but it's better this way.
    file_list = os.listdir("temp/input")
    num_files = len(file_list)
    i = 0

    for file in file_list:
        
        current_progress = int((i / num_files) * 100)

        #update progress every 5%
        if current_progress % 5 == 0:
            print(str(current_progress) + '% complete', end="\r")
            
        #open the jpeg of the frame, sort it, and store it as sorted_frame
        sorted_frame = sort_image(Image.open("temp/input/" + file))

        #save the sorted frame to a temporary output directory
        sorted_frame.save("temp/output/" + file)

        i += 1

    print("Done!")
    
    print("Converting sorted frames to video. . . ", end = "")
    #convert the images from the temporary output directory to a video
    os.system("ffmpeg -framerate 30 -i temp/output/frame_%05d.jpeg output.mp4 >> /dev/null 2>&1")
    print("Done!")

    print("Cleaning up. . . ", end = "")
    #finally, delete our temporary folder
    shutil.rmtree("temp")

    print("Done!")


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
    if os.path.isfile(argv[1]):

        file_extension = os.path.splitext(argv[1])[1].lower()
        if file_extension in IMG_FORMATS:
            image_handler(Image.open(argv[1]))

        elif file_extension in VID_FORMATS:
            video_handler(argv[1])

main()
