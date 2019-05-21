from PIL import Image

pathTo = "change this"
def getImage(fileName):
    try:
        fullPath = pathTo+fileName
        img = Image.open(fullPath)

    except IOError:
        print('IMAGE GRAB ERROR: Could not open file: ' + fullPath)

def main():
    image = raw_input("Enter image name ")
    getImage(image)

if __name__ == "__main__":
    main()
