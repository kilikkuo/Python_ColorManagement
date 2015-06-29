# D50 <=> D65
#http://ninedegreesbelow.com/photography/srgb-color-space-to-profile.html
#http://www.brucelindbloom.com/index.html?Eqn_ChromAdapt.html


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
    return tags

#meta = get_exif_by_exifread(fPath)
#print meta.get('EXIF ColorSpace', 0)
#meta = get_exif_by_PIL(fPath)
#print meta