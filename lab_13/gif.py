import Image
import sys
import numpy

numero = 0
color = (0, 255, 137)

def readGif(filename):
    # This metod was taken of...
    # https://code.google.com/p/python-learning-tools/source/browse/trunk/images2gif.py
    """ readGif(filename, asNumpy=True)
    Read images from an animated GIF file.  Returns a list of numpy 
    arrays, or, if asNumpy is false, a list if PIL images.
    """
    
    # Load file using PIL
    pilIm = Image.open(filename)   
    pilIm.seek(0)
    
    # Read all images inside
    images = []
    try:
        while True:
            # Get image as numpy array
            tmp = pilIm.convert() # Make without palette
            a = numpy.asarray(tmp)
            if len(a.shape)==0:
                raise MemoryError("Too little memory to convert PIL image to array")
            # Store, and next
            images.append(tmp)
            pilIm.seek(pilIm.tell()+1)
    except EOFError:
        pass
    
    # Done
    return images

def difference(ima, ima2, UMBRAL=50):
    ''' 
        You create a new image and the values of its pixels is the difference
        of tha images selected.
    '''
    global numero
    global color

    w = ima.size[0] # take a image of the list and get its dimensions
    h = ima.size[1]

    pix = ima.load() # load pixels
    pix2 = ima2.load() # load pixels

    # create a new image that will be the difference of both pixeles. 
    # To see the moviment.
    newImage = Image.new('RGB', (w,h))
    newPix = newImage.load()
    
    for y in range(h):
        for x in range(w):
            if(pix2[x,y][0] - pix[x,y][0]) > UMBRAL:
                newPix[x,y] = color # there was movement
            else:
                newPix[x,y] = pix[x,y] # stays the same

    newImage.save(str(numero+1)+'.png') # save the file
    numero += 1
    return newImage


def detectMotion(images):
    print 'Looking for differences in pixeles...'
 
    motionPixels = list()
    for i in range(len(images)-1):
        newImage = difference(images[i], images[i+1])
        motionPixels.append(newImage)
    print 'READY'
    return motionPixels


def main(nombreGif):
    # read the gif
    images = readGif(nombreGif)

    # play with scanned images
    motionPixels = detectMotion(images)


##### Parametros del programa ####
#[1] = gif name
##################################
main(sys.argv[1])


