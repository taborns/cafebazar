from PIL import Image
import requests
IMAGE_PATH = '/Users/mac/Downloads/'
def convertWebp(url, size=(100,100)):
    import random
    randnum = random.randint(1000,10000)

    image_name = url.split('/')[-1].split('.')[0]
    image_name = image_name + str(randnum) + '.webp'
    image = Image.open(requests.get(url, stream=True).raw)
    image.thumbnail(size, Image.ANTIALIAS)
    image.save(IMAGE_PATH + 'compressedo-' + image_name, 'webp', optimize=True)

    return image_name

url = 'https://s.cafebazaar.ir/1/icons/air.org.axisentertainment.BabyHazelLearnsShapes_512x512.png'

print convertWebp(url)