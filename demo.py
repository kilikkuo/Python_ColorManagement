import numpy
import pyopencl as cl
import math
from time import time, sleep
from PIL import Image

def loadImage(path):
    img = Image.open(path)
    print "-" * 20
    print "Image Informatio : Format(%s), Size(%s), Mode(%s)\n"\
        %(img.format, img.size, img.mode)
    print "-" * 20
    return img

def rgb_to_XYZ_to_rgb_cpu(image):
    ld = image.load()
    w, h = image.size
    # D65 wp
    Xn = 0.95047
    Yn = 1.00000
    Zn = 1.08883

    sRGBtoXYZ = [[0.4124564, 0.3575761, 0.1804375], 
                 [0.2126729, 0.7151522, 0.0721750],
                 [0.0193339, 0.1191920, 0.9503041]]
    XYZtosRGB = [[3.2404542, -1.5371385, -0.4985314],
                 [-0.9692660, 1.8760108, 0.0415560],
                 [0.0556434, -0.2040259, 1.0572252]]
    
    def gammaDecode(normColor):
        gamma = 2.2
        return normColor ** (gamma)
    def gammaEncode(normColor):
        gamma = 2.2
        return normColor ** (1.0/gamma)
    def normalizeColor(color):
        return color / 255.0
    def denormalizeTo8bit(normValue):
        return min(255, max(0, int(normValue * 255)))

    for y in range(h):
        for x in range(w):
            R,G,B = ld[x,y]
            nR, nG, nB = normalizeColor(R), normalizeColor(G), normalizeColor(B)
            nLR, nLG, nLB = gammaDecode(nR), gammaDecode(nG), gammaDecode(nB)

            X = sum(map(lambda x,y: x*y, [nLR, nLG, nLB], sRGBtoXYZ[0]))
            Y = sum(map(lambda x,y: x*y, [nLR, nLG, nLB], sRGBtoXYZ[1]))
            Z = sum(map(lambda x,y: x*y, [nLR, nLG, nLB], sRGBtoXYZ[2]))

            nLR2 = sum(map(lambda x,y:x*y, [X, Y, Z], XYZtosRGB[0]))
            nLG2 = sum(map(lambda x,y:x*y, [X, Y, Z], XYZtosRGB[1]))
            nLB2 = sum(map(lambda x,y:x*y, [X, Y, Z], XYZtosRGB[2]))

            nGER = gammaEncode(nLR2)
            nGEG = gammaEncode(nLG2)
            nGEB = gammaEncode(nLB2)

            ld[x,y] = denormalizeTo8bit(nGER), denormalizeTo8bit(nGEG), denormalizeTo8bit(nGEB)

    image.show()

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
    img = loadImage("./Sample.JPG")

    #rgb_to_yuv_to_rgb_gpu(img)
    #rgb_to_yuv_to_rgb_cpu(img)
    rgb_to_XYZ_to_rgb_cpu(img)
    pass

if __name__ == '__main__':
    main()