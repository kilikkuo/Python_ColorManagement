import numpy
import pyopencl as cl
import math
from time import time, sleep
from PIL import Image
from ColorChannelInst import ColorChannelInstance, DisplayCCInst
from EXIF_ColorProfileParser import get_exif_by_exifread, get_exif_by_PIL
from RGB_XYZ import XYZtoRGB, RGBtoXYZ

def loadImage(path):
    img = Image.open(path)
    print "-" * 20
    print "Image Information : Format(%s), Size(%s), Mode(%s)\n"\
        %(img.format, img.size, img.mode)
    print "-" * 20
    return img

def rgb_to_yuv_to_rgb_cpu(image):
    ld = image.load()
    w, h = image.size
    for y in range(h):
        for x in range(w):
            R,G,B = ld[x,y]
            Y = 0.299*R + 0.587*G + 0.114*B
            U = -0.147*R - 0.289*G + 0.436*B
            V = 0.615*R - 0.515*G - 0.100*B
            r = min(255, max(0, int(Y + 1.14*V)))
            g = min(255, max(0, int(Y - 0.39*U - 0.58*V)))
            b = min(255, max(0, int(Y + 2.03*U)))
            ld[x,y] = r,g,b
    image.show()
    pass

def rgb_to_yuv_to_rgb_gpu(img):
    from ColorManagement import ColorManagement
    cmm = ColorManagement()

    imgSize = img.size[0] * img.size[1]
    bufferIn = cmm.createBufferData(ColorManagement.RGBPixel, lstData=img.getdata())
    bufferOut = cmm.createBufferData(ColorManagement.YUVPixel, imgSize)

    final = cmm.createBufferData(ColorManagement.RGBPixel, imgSize)
    cmm.rgb_to_yuv((img.size[0], img.size[1]), None,\
                   img.size[0], img.size[1], bufferIn, bufferOut)

    cmm.yuv_to_rgb((img.size[0], img.size[1]), None,\
                   img.size[0], img.size[1], bufferOut, final)
    result = final.reshape(img.size[1], img.size[0]).get()

    img = Image.fromarray(result, 'RGB')
    img.show()
    pass

def main():
    fPath = "./Sample.JPG"
    img = loadImage(fPath)
    oriImg = ColorChannelInstance(img.size[0], img.size[1], img)
    DisplayCCInst(XYZtoRGB(RGBtoXYZ(oriImg)))
    #rgb_to_yuv_to_rgb_gpu(img)
    #rgb_to_yuv_to_rgb_cpu(img)
    pass

if __name__ == '__main__':
    main()