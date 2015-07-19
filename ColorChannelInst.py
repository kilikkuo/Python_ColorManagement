import PIL
from PIL import Image

WPD65 = 'D65'
WPD50 = 'D50'

WORKSPACE_CIEXYZ        = 'CIEXYZ'
WORKSPACE_sRGB          = 'sRGB'
WORKSPACE_AdobeRGB      = 'AdobeRGB'
WORKSPACE_ProPhotoRGB   = 'ProPhotoRGB'

def DisplayCCInst(ccInst):
    img = Image.new('RGB', ccInst.size)
    img.putdata(ccInst.data)
    img.show()

class ColorChannelInstance:
    def __init__(self, width, height, img=None, comp='RGB', ws='sRGB', wp=WPD65):
        self.data = []
        if img and img.__class__.__name__ in ["JpegImageFile", "PngImageFile"]:
            assert ((width, height)==img.size)
            self.data = list(img.getdata())

        self.__width = width
        self.__height = height
        self.__whitePoint = wp
        self.size = self.__width, self.__height
        self.mode = comp
        self.__workSpace = ws
        if len(self.data)==0 and not img:
            self.data = [(0,0,0)]*width*height

    def getWhitePoint(self):
        return self.__whitePoint

    def getWorkSpace(self):
        return self.__workSpace

    def __getitem__(self, tupIndex):
        assert (type(tupIndex)==tuple and len(tupIndex)==2)
        x, y = tupIndex
        return self.data[y*self.__width+x]

    def __setitem__(self, tupIndex, value):
        assert (type(tupIndex)==tuple and len(tupIndex)==2)
        x, y = tupIndex
        self.data[y*self.__width+x] = value
