import numpy
import pyopencl as cl
import math
from time import time, sleep
from PIL import Image
from ColorChannelInst import ColorChannelInstance, displayCCInst, WPD50, WPD65,\
                             WORKSPACE_sRGB, WORKSPACE_ProPhotoRGB, WORKSPACE_AdobeRGB,\
                             createCCInstTemp
from EXIF_ColorProfileParser import get_metadata_by_exiftool
from RGB_XYZ import XYZtoRGB, RGBtoXYZ, XYZ_WPTransform

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
    # Set demoAdobeRGB2sRGB=True is to verify that the python CMM transformation
    # result is correct as using pillImageCms
    demoAdobeRGB2sRGB = False
    demosRGB2ProphotoRBG = not demoAdobeRGB2sRGB

    fPath = "./Sample.JPG" if not demoAdobeRGB2sRGB else "./images/tampa_AdobeRGB.jpg"
    # TODO : Leverage metadata parser to identify the color space information
    oriImg = createCCInstTemp(fPath, demoAdobeRGB2sRGB)
    #displayCCInst(oriImg)

    xyzFromOriginWP = RGBtoXYZ(oriImg)

    xyzToTargetWP = None
    if demoAdobeRGB2sRGB:
        xyzToTargetWP = XYZ_WPTransform(xyzFromOriginWP, targetWP=WPD65)
    else:
        if demosRGB2ProphotoRBG:
            #xyzToTargetWP = XYZ_WPTransform(xyzFromOriginWP, targetWP=WPD50)
            xyzToTargetWP = XYZ_WPTransform(xyzFromOriginWP, targetWP=WPD65)
        else:
            assert False, "Not decided yet."

    newRGB = None
    if demoAdobeRGB2sRGB:
        newRGB = XYZtoRGB(xyzToTargetWP, ws=WORKSPACE_sRGB, wp=WPD65)
    else:
        #newRGB = XYZtoRGB(xyzToTargetWP, ws=WORKSPACE_ProPhotoRGB, wp=WPD50)
        newRGB = XYZtoRGB(xyzToTargetWP, ws=WORKSPACE_sRGB, wp=WPD65)
    displayCCInst(newRGB)

    # A implementation to test rgb to yuv to rgb performance
    #img = loadImage(fPath)
    #rgb_to_yuv_to_rgb_gpu(img)
    #rgb_to_yuv_to_rgb_cpu(img)
    pass

if __name__ == '__main__':
    main()
