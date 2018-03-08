import PIL
import matplotlib.pyplot as plt # single use of plt is commented out
import os.path  
import PIL.ImageDraw            

def frame(original_image, color, percent_of_side):
    """ Places a frame around a PIL.Image
    Change line 37 so that use_decorative_frame is False to answer Step 10.
    original_image must be a PIL.Image
    Returns a new PIL.Image with a border, where
    0 < percent_of_side < 1
    is the border width as a portion of the shorter dimension of original_image
    """
    #set the radius of the rounded corners
    width, height = original_image.size
    thickness = int(percent_of_side * min(width, height)) # thickness in pixels
    
    ###
    #create a mask
    ###
    
    #start with alpha=0 mask
    r, g, b = color
    frame_mask = PIL.Image.new('RGBA', (width, height), (0, 0, 0, 0))
    drawing_layer = PIL.ImageDraw.Draw(frame_mask)
    
    # Draw four rectangles to fill frame area with alpha=255
    drawing_layer.rectangle((0, 0, width, thickness), fill=(r, g, b, 255)) #top
    drawing_layer.rectangle((0, 0, thickness, height), fill=(r, g, b, 255)) # left
    drawing_layer.rectangle((0, height, width, height-thickness), fill=(r, g, b, 255)) # bottom
    drawing_layer.rectangle((width, 0, width-thickness, height), fill=(r, g, b, 255)) #right
    
    # Make the new image, starting with all transparent
    #frame_image = PIL.Image.new('RGBA', (width, height), (r, g, b, 255))
    crest = PIL.Image.open(os.path.join(os.getcwd(), 'farkas.jpeg')) #Includes family crest, which is 'farkas.jpeg'
    crest_size = ((height/9))
    small_crest = crest.resize((crest_size,crest_size))
    result = original_image.copy()
    use_decorative_frame = True
    if use_decorative_frame: 
        frame_pic = PIL.Image.open(os.path.join(os.getcwd(), 'frame.jpg'))
        frame_pic = frame_pic.resize(result.size)
        result.paste(frame_pic, (0,0), mask=frame_mask)
        result.paste(small_crest, ((width/2)-(crest_size/2),(height-(crest_size))))
    else:
        result.paste(frame_mask, (0,0), mask=frame_mask)
    return result
    
def get_images(directory=None):
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
    
def frameimageswithcrest(directory=None, color=(255,0,0), width=0.10):
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
        new_image = frame(image_list[n],color, width)
        #save the altered image, suing PNG to retain transparency
        new_image_filename = os.path.join(new_directory, filename + '.png')
        new_image.save(new_image_filename)     