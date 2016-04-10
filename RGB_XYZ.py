from ColorChannelInst import ColorChannelInstance, WPD65, WPD50
from EXIF_ColorProfileParser import getChromaticAdaptationMat
"""
 D65 =====================================================
"""

sRGBtoXYZ_D65 = [[0.4124564, 0.3575761, 0.1804375],
                 [0.2126729, 0.7151522, 0.0721750],
                 [0.0193339, 0.1191920, 0.9503041]]

XYZtosRGB_D65 = [[3.2404542, -1.5371385, -0.4985314],
                 [-0.9692660, 1.8760108, 0.0415560],
                 [0.0556434, -0.2040259, 1.0572252]]

AdobeRGBtoXYZ_D65 = [[0.5767309, 0.1855540, 0.1881852],
                     [0.2973769, 0.6273491, 0.0752741],
                     [0.0270343, 0.0706872, 0.9911085]]

XYZtoAdobeRGB_D65 = [[2.0413690, -0.5649464, -0.3446944],
                     [-0.9692660, 1.8760108, 0.0415560],
                     [0.0134474, -0.1183897, 1.0154096]]
"""
 D50 =====================================================
"""

sRGBtoXYZ_D50 = [[0.4360747, 0.3850649, 0.1430804],
                 [0.2225045, 0.7168786, 0.0606169],
                 [0.0139322, 0.0971045, 0.7141733]]

XYZtosRGB_D50 = [[3.1338561, -1.6168667, -0.4906146],
                 [-0.9787684, 1.9161415, 0.0334540],
                 [0.0719453, -0.2289914, 1.4052427]]

AdobeRGBtoXYZ_D50 = [[0.6097559, 0.2052401, 0.1492240],
                     [0.3111242, 0.6256560, 0.0632197],
                     [0.0194811, 0.0608902, 0.7448387]]

XYZtoAdobeRGB_D50 = [[1.9624274, -0.6105343,-0.3413404],
                     [-0.9787684, 1.9161415, 0.0334540],
                     [0.0286869, -0.1406752, 1.3487655]]

ProPhototoXYZ_D50 = [[0.7976749, 0.1351917, 0.0313534],
                     [0.2880402, 0.7118741, 0.0000857],
                     [0.0000000, 0.0000000, 0.8252100]]

XYZtoProPhoto_D50 = [[1.3459433, -0.2556075, -0.0511118],
                     [-0.5445989, 1.5081673, 0.0205351],
                     [0.0000000, 0.0000000, 1.2118128]]

dicWPRGBtoXYZMatrix = { WPD65 : { 'sRGB'        : sRGBtoXYZ_D65,
                                  'AdobeRGB'    : AdobeRGBtoXYZ_D65},
                        WPD50 : { 'sRGB'        : sRGBtoXYZ_D50,
                                  'AdobeRGB'    : AdobeRGBtoXYZ_D50,
                                  'ProPhotoRGB' : ProPhototoXYZ_D50}}

dicWPXYZtoRGBMartix = { WPD65 : { 'sRGB'        : XYZtosRGB_D65,
                                  'AdobeRGB'    : XYZtoAdobeRGB_D65},
                        WPD50 : { 'sRGB'        : XYZtosRGB_D50,
                                  'AdobeRGB'    : XYZtoAdobeRGB_D50,
                                  'ProPhotoRGB' : XYZtoProPhoto_D50}}

dictGammaValue = { 'sRGB'           : 2.2,
                   'AdobeRGB'       : 2.2,
                   'ProPhotoRGB'    : 1.8 }

def gammaDecode(normColor, gamma=2.2):
    return normColor ** (gamma)

def gammaEncode(normColor, gamma=2.2):
    return normColor ** (1.0/gamma)

def normalizeColor(color):
    assert (type(color)==int and 0 <= color <= 255)
    return color / 255.0

def denormalizeTo8bit(normValue):
    return min(255, max(0, int(normValue * 255)))

def fixNormalBoundary(value):
    return max(0.0, min(1.0, value))

def RGBtoXYZ(ccInst):
    w, h = ccInst.size[0], ccInst.size[1]
    inputWP = ccInst.getWhitePoint()
    inputWS = ccInst.getWorkSpace()

    matrix = dicWPRGBtoXYZMatrix.get(inputWP, {}).get(inputWS, {})
    inputGamma = dictGammaValue.get(inputWS, 0)

    if not matrix or inputGamma == 0:
        assert False, "No matching inputr matrix - %s / %s / %f "%(inputWS, inputWP, inputGamma)
        return None

    newCCInst = ColorChannelInstance(w, h, None, comp='XYZ', ws='CIEXYZ', wp=inputWP)
    for y in range(h):
        for x in range(w):
            R,G,B = ccInst[x,y]
            nR, nG, nB = normalizeColor(R), normalizeColor(G), normalizeColor(B)
            nLR = gammaDecode(nR, inputGamma)
            nLG = gammaDecode(nG, inputGamma)
            nLB = gammaDecode(nB, inputGamma)

            X = sum(map(lambda x,y: x*y, [nLR, nLG, nLB], matrix[0]))
            Y = sum(map(lambda x,y: x*y, [nLR, nLG, nLB], matrix[1]))
            Z = sum(map(lambda x,y: x*y, [nLR, nLG, nLB], matrix[2]))
            newCCInst[x,y] = X,Y,Z

    return newCCInst

def XYZ_WPTransform(ccInst, targetWP=WPD65):
    w, h = ccInst.size[0], ccInst.size[1]
    inputWP = ccInst.getWhitePoint()
    matrix = getChromaticAdaptationMat('Bradford', inputWP, targetWP)

    if inputWP == targetWP:
        print "Input white point is the same as target white point, no need to transform"
        return ccInst
    if not matrix:
        print "No chromatic adaptation matrix found, do NOT transform"
        return ccInst

    newCCInst = ColorChannelInstance(w, h, None, comp='XYZ', ws='CIEXYZ', wp=targetWP)
    for y in range(h):
        for x in range(w):
            Xs, Ys, Zs = ccInst[x,y]

            Xd = sum(map(lambda x,y:x*y, [Xs, Ys, Zs], matrix[0]))
            Yd = sum(map(lambda x,y:x*y, [Xs, Ys, Zs], matrix[1]))
            Zd = sum(map(lambda x,y:x*y, [Xs, Ys, Zs], matrix[2]))

            newCCInst[x,y] = Xd, Yd, Zd

    return newCCInst

def XYZtoRGB(ccInst, ws='sRGB', wp=None):
    w, h = ccInst.size[0], ccInst.size[1]
    inputWP = ccInst.getWhitePoint()
    targetWP = wp if wp != None else inputWP
    targetWS = ws if ws != 'sRGB' else 'sRGB'
    newCCInst = ColorChannelInstance(w, h, None, comp='RGB', ws=targetWS, wp=targetWP)

    matrix = dicWPXYZtoRGBMartix.get(targetWP, {}).get(targetWS, {})
    targetGamma = dictGammaValue.get(targetWS, 0)

    if not matrix or targetGamma == 0:
        assert False, "No matching target matrix - %s / %s / %f "%(targetWS, targetWP, targetGamma)
        return None

    for y in range(h):
        for x in range(w):
            X,Y,Z = ccInst[x,y]

            nLR2 = fixNormalBoundary(sum(map(lambda x,y:x*y, [X, Y, Z], matrix[0])))
            nLG2 = fixNormalBoundary(sum(map(lambda x,y:x*y, [X, Y, Z], matrix[1])))
            nLB2 = fixNormalBoundary(sum(map(lambda x,y:x*y, [X, Y, Z], matrix[2])))

            nGER = gammaEncode(nLR2, targetGamma)
            nGEG = gammaEncode(nLG2, targetGamma)
            nGEB = gammaEncode(nLB2, targetGamma)

            newCCInst[x,y] = denormalizeTo8bit(nGER), denormalizeTo8bit(nGEG), denormalizeTo8bit(nGEB)

    return newCCInst
