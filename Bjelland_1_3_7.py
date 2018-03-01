import PIL
import matplotlib.pyplot as plt # single use of plt is commented out
import os.path  
import PIL.ImageDraw            

def frame(original_image, color, frame_width):
    """ Frames the image with the specified color and width of a PIL.Image

    original_image must be a PIL.Image
    Returns a new PIL.Image with a frame, where
    0 < frame_width < 1

    """
    #set the width of the frame
    width, height = original_image.size
    thickness = int(frame_width * min(width, height)) # radius in pixels

    ###
    #create a mask
    ###

    #start with transparent mask
    r,g,b = color
    frame_mask = PIL.Image.new('RGBA', ((1.25 * float (width)), (1.25 * float (height))), (0,0,0,0))
    drawing_layer = PIL.ImageDraw.Draw(frame_mask)
    
    # Overwrite the RGBA values with A=255.
    # The 127 for RGB values was used merely for visualizing the mask
    
    # Draw two rectangles to fill interior with opaqueness
    drawing_layer.rectangle((0-thickness,0-thickness,width+thickness,thickness), fill=(r,g,b,255)) #top rectangle. Outside 
    drawing_layer.rectangle((0,0-thickness,0-thickness,height-thickness), fill=(r,g,b,255)) #left rectangle
    drawing_layer.rectangle((0-thickness,height,width+thickness,height+thickness), fill=(r,g,b,255)) #bottom rectangle
    drawing_layer.rectangle((width,0-thickness,width+thickness,height+thickness), fill=(r,g,b,255)) #right rectangle

    # Make the new image, starting with all transparent
    #frame_image = PIL.Image.new('RGBA', (width, height), (r,g,b,255))
    result = original_image.copy()
    result.paste(frame_mask, (0,0), mask=frame_mask)
    return result

def get_images(directory='1.4.5 Images'):
    """ Returns PIL.Image objects for all the images in directory.

    If directory is not specified, uses current directory.
    Returns a 2-tuple containing 
    a list with a  PIL.Image object for each image file in root_directory, and
    a list with a string filename for each image file in root_directory
    """

    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    image_list = [] # Initialize aggregaotrs
    file_list = []

    directory_list = os.listdir(directory) # Get list of files
    for entry in directory_list:
        absolute_filename = os.path.join(directory, entry)
        try:
            image = PIL.Image.open(absolute_filename)
            file_list += [entry]
            image_list += [image]
        except IOError:
            pass # do nothing with errors tying to open non-images
    return image_list, file_list

def frame_all_images(directory=None, color=(255,215,0), frame_width=0.1): #color gold
    """ Saves a modfied version of each image in directory.

    Uses current directory if no directory is specified. 
    Places images in subdirectory 'modified', creating it if it does not exist.
    New image files are of type PNG and have transparent rounded corners.
    """

    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
  
    # Create a new directory 'modified'
    new_directory = os.path.join(directory, 'modified')
    try:
        os.mkdir(new_directory)
    except OSError:
        pass # if the directory already exists, proceed  

    #load all the images
    image_list, file_list = get_images(directory)  

    #go through the images and save modified versions
    for n in range(len(image_list)):
        # Parse the filename
        filename, filetype = file_list[n].split('.')
        print n
        # Round the corners with radius = 30% of short side
        new_image = frame(image_list[n],color, frame_width)
        #save the altered image, suing PNG to retain transparency
        new_image_filename = os.path.join(new_directory, filename + '.png')
        new_image.save(new_image_filename)    