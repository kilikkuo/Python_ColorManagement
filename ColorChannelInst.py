import PIL
from PIL import Image

def DisplayCCInst(ccInst):
    img = Image.new('RGB', ccInst.size)
    img.putdata(ccInst.data)
    img.show()

class ColorChannelInstance:
    def __init__(self, width, height, img=None, comp='RGB', ws='sRGB'):
        self.data = []
        if img and img.__class__.__name__ in ["JpegImageFile", "PngImageFile"]:
            assert ((width, height)==img.size)
            self.data = list(img.getdata())

        self.__width = width
        self.__height = height
        self.size = self.__width, self.__height
        self.mode = comp
        self.workSpace = ws
        if len(self.data)==0 and not img:
            self.data = [(0,0,0)]*width*height

    def __getitem__(self, tupIndex):
        assert (type(tupIndex)==tuple and len(tupIndex)==2)
        x, y = tupIndex
        return self.data[y*self.__width+x]

    def __setitem__(self, tupIndex, value):
        assert (type(tupIndex)==tuple and len(tupIndex)==2)
        x, y = tupIndex
        self.data[y*self.__width+x] = value