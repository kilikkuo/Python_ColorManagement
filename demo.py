import numpy
import pyopencl as cl
import math
from time import time, sleep
from PIL import Image
from ColorChannelInst import ColorChannelInstance, displayCCInst, WPD50, WPD65,\
                             WORKSPACE_sRGB, WORKSPACE_ProPhotoRGB, WORKSPACE_AdobeRGB,\
                             createCCInstTemp
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

def main(iPath, tWS, tWP, oPath=None):
    assert iPath != None, "Input file is required !"

    oriImg = createCCInstTemp(iPath)
    #displayCCInst(oriImg)

    xyzFromOriginWP = RGBtoXYZ(oriImg)

    xyzToTargetWP = XYZ_WPTransform(xyzFromOriginWP, targetWP=tWP)

    newRGB = XYZtoRGB(xyzToTargetWP, ws=tWS, wp=tWP)
    displayCCInst(newRGB)

    if oPath != None:
        oImg = Image.new('RGB', ccInst.size)
        oImg.putdata(ccInst.data)
        oImg.save(oPath)

    # A implementation to test rgb to yuv to rgb performance
    #img = loadImage(iPath)
    #rgb_to_yuv_to_rgb_gpu(img)
    #rgb_to_yuv_to_rgb_cpu(img)
    pass

import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input file to be converted')
    parser.add_argument('-ocs', '--output-colorspace', help='Color space for output file(default:WORKSPACE_sRGB)', default=WORKSPACE_sRGB)
    parser.add_argument('-owp', '--output-whitepoint', help='Ref White point for output file(default:WPD65)', default=WPD65)
    parser.add_argument('-o', '--output', help='Output file for convreted result, e.g. /PATH_TO_OUTPUT/FILENAME.EXT')
    args = parser.parse_args()

    main(args.input, args.output_colorspace, args.output_whitepoint, args.output)
