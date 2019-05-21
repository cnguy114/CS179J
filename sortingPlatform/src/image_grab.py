from PIL import Image

pathTo = "change this"
def grabImage(fileName):
    fullPath = pathTo+fileName
    try:
        img = Image.open(fullPath)
    except IOERROR:
        print 'ERROR IN grabImage()... Could not open file: ' + fullPath
