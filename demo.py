import numpy
import pyopencl as cl
from time import time
from PIL import Image

def PIL2array(img):
    return numpy.array(img.getdata(),
        numpy.uint8).reshape(img.size[1], img.size[0], 3)

def Array2PILImage(arrBuf):
    print "Final[0] : ", arrBuf[0][0]
    print "Final[1] : ", arrBuf[1][0]
    print "Final[2] : ", arrBuf[2][0]
    im = Image.fromarray(arrBuf)
    im.save("./test.jpg")

def loadImage(path):
    img = Image.open(path)
    print "-" * 20
    print "Image Informatio : Format(%s), Size(%s), Mode(%s)\n"\
        %(img.format, img.size, img.mode)
    print "-" * 20
    imgArr = PIL2array(img)
    return imgArr

def OCL_CMM(pixelsArray):
    shape = pixelsArray.shape
    print " Pixels Array Shape : ", shape

    clContext = cl.create_some_context()
    clQueue = cl.CommandQueue(clContext)

    pixelsCount = shape[0] * shape[1] * shape[2]
    globalSize = ((pixelsCount + 15) << 4) >> 4
    print " Pixels Count  : ", pixelsCount
    print " Global Size  : ", globalSize
    print " Pixel[0][0] : ", pixelsArray[0][0]

    fstr = ''.join(open("cmm.cl", "r").readlines())
    clProgram = cl.Program(clContext, fstr).build()
    
    bufIn = cl.Buffer(clContext, cl.mem_flags.READ_ONLY | \
        cl.mem_flags.USE_HOST_PTR, hostbuf=pixelsArray)
    bufOut = cl.Buffer(clContext, cl.mem_flags.WRITE_ONLY | \
        cl.mem_flags.USE_HOST_PTR, hostbuf=pixelsArray)
    clProgram.cmm(clQueue, (globalSize,), None, \
        numpy.uint32(pixelsCount), bufIn, bufOut)

    finalBuf = numpy.zeros(shape, dtype=numpy.uint8)
    evt = cl.enqueue_read_buffer(clQueue, bufOut, finalBuf)
    evt.wait()

    Array2PILImage(finalBuf)
    pass

def main():
    pixlesArray = loadImage("./Sample.JPG")
    OCL_CMM(pixlesArray)
    pass

main()