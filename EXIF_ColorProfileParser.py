# D50 <=> D65
#http://ninedegreesbelow.com/photography/srgb-color-space-to-profile.html
#http://www.brucelindbloom.com/index.html?Eqn_ChromAdapt.html
import os
from ColorChannelInst import WPD65, WPD50

D65toD50_XYZScaling = [[1.0144665, 0.0000000, 0.0000000],
                       [0.0000000, 1.0000000, 0.0000000],
                       [0.0000000, 0.0000000, 0.7578869]]

D65toD50_Bradford = [[1.0478112, 0.0228866, -0.0501270],
                     [0.0295424, 0.9904844, -0.0170491],
                     [-0.0092345, 0.0150436, 0.7521316]]

D50toD65_XYZScaling = [[0.9857398, 0.0000000, 0.0000000],
                       [0.0000000, 1.0000000, 0.0000000],
                       [0.0000000, 0.0000000, 1.3194581]]

D50toD65_Bradford = [[0.9555766, -0.0230393, 0.0631636],
                     [-0.0282895, 1.0099416, 0.0210077],
                     [0.0122982, -0.0204830, 1.3299098]]

dicXYZScaling = { WPD65 : { WPD50 : D65toD50_XYZScaling },
                  WPD50 : { WPD65 : D50toD65_XYZScaling }}
dicBradford = { WPD65 : { WPD50 : D65toD50_Bradford },
                WPD50 : { WPD65 : D50toD65_Bradford }}

CHROMATIC_ADAPTION_XYZSCALING     = 'XYZScaling'
CHROMATIC_ADAPTION_BRADFORD       = 'Bradford'

dicChromaticAdaptation = { CHROMATIC_ADAPTION_XYZSCALING : dicXYZScaling,
                           CHROMATIC_ADAPTION_BRADFORD   : dicBradford}

def getChromaticAdaptationMat(method, fromWP, toWP):
    if fromWP == toWP:
        return []
    mat = dicChromaticAdaptation.get(method, {}).get(fromWP, {}).get(toWP, [])
    return mat

# exif tag definition.
#http://www.media.mit.edu/pia/Research/deepview/exif.html

def get_exif_by_PIL(filePath):
    from PIL import Image
    from PIL.ExifTags import TAGS
    img = Image.open(filePath)
    ret = {}
    info = img._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

def get_exif_by_exifread(filePath):
    import exifread
    tags = exifread.process_file(open(filePath))
    #print "CS = ", tags.get('EXIF ColorSpace', 0)
    #print "WP = ", tags.get('WhitePoint', 0)
    return tags

def get_metadata_by_exiftool(filePath):
    # http://www.sno.phy.queensu.ca/~phil/exiftool/index.html
    # TODO : Need to obtain TRC(tone responsive curve) by other commands further

    from subprocess import call, Popen, PIPE
    dicMeta = {}
    try:
        obj = Popen(["./Image-ExifTool-10.15/exiftool", "-t", filePath], stdout=PIPE, stderr=PIPE)
        data = obj.communicate()

        import re
        from itertools import izip
        splittedData = re.split('\t|\n',data[0])
        def pairwise(iterable):
            "s -> (s0, s1), (s2, s3), (s4, s5), ..."
            item = iter(iterable)
            return izip(item, item)
        dicMeta = {}
        for k, v in pairwise(splittedData):
            dicMeta[k] = v
    except:
        import traceback
        traceback.print_exc()
    # Key will be used
    # - "Color Space"
    # - "ICC Profile Name"
    # - "Media White Point"
    # - "Profile Description"
    # - "Rendering Intent"
    # - "Profile Connection Space"
    return dicMeta

"""
fPath = "./Sample.JPG"
fPath = "./images/tampa_AdobeRGB.jpg"
fullPath = os.path.abspath(fPath)
print fullPath
meta = get_metadata_by_exiftool(fullPath)
print meta
"""
