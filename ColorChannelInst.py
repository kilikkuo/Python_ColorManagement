import PIL
from PIL import Image

WPD65 = 'D65'
WPD50 = 'D50'

WORKSPACE_CIEXYZ        = 'CIEXYZ'
WORKSPACE_sRGB          = 'sRGB'
WORKSPACE_AdobeRGB      = 'AdobeRGB'
WORKSPACE_ProPhotoRGB   = 'ProPhotoRGB'

def displayCCInst(ccInst):
    img = Image.new('RGB', ccInst.size)
    img.putdata(ccInst.data)
    img.show()

def loadImage(path):
    img = Image.open(path)
    print "-" * 20
    print "Image Information : Format(%s), Size(%s), Mode(%s)\n"\
        %(img.format, img.size, img.mode)
    print "-" * 20
    return img

def createCCInstTemp(fPath):
    return createColorChannelInstance(fPath=fPath)

def createColorChannelInstance(fPath=None, imgData=None, package={}):
    assert not (fPath == None and imgData == None and package == {})
    ccInst = None
    if fPath and not imgData and not package:
        from EXIF_ColorProfileParser import get_metadata_by_exiftool,\
            getWPByWPMatrix, LIST_sRGB_D65_WHITE_POINT
        img = loadImage(fPath)
        meta = get_metadata_by_exiftool(fPath)

        ws = meta.get('Color Space', None)
        if meta.get('Color Space', None) == 0:
            ws = WORKSPACE_sRGB
        elif meta.get('Color Space', None) == "Uncalibrated":
            pDesc = meta.get('Profile Description', None)
            iccProfileName = meta.get('ICC Profile Name', None)
            if pDesc.find('Adobe RGB') >=0 or iccProfileName.find('Adobe RGB') >= 0:
                ws = WORKSPACE_AdobeRGB

        strMWP = meta.get('Media White Point',\
                          ' '.join(str(item) for item in LIST_sRGB_D65_WHITE_POINT))
        mwp = getWPByWPMatrix(strMWP)

        ccInst = ColorChannelInstance(img.size[0], img.size[1], img, ws=ws, wp=mwp)
    elif imgData and not fPath and not package:
        ccInst = ColorChannelInstance(imgData.size[0], imgData.size[1], imgData)
    elif package and not imgData and not fPath:
        w = package.get('w', 0)
        h = package.get('h', 0)
        comp = package.get('comp', 'RGB')
        wp = package.get('wp', WPD65)
        ws = package.get('ws', WORKSPACE_sRGB)
        ccInst = ColorChannelInstance(w, h, None, comp=comp, ws=ws, wp=wp)
        pass

    assert ccInst, "ColorChannelInstance can't be created."
    return ccInst

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
