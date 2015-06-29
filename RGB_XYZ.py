from ColorChannelInst import ColorChannelInstance, WPD65, WPD50

"""
 D65 =====================================================
"""

sRGBtoXYZ_D65 = [[0.4124564, 0.3575761, 0.1804375],
                 [0.2126729, 0.7151522, 0.0721750],
                 [0.0193339, 0.1191920, 0.9503041]]
XYZtosRGB_D65 = [[3.2404542, -1.5371385, -0.4985314],
                 [-0.9692660, 1.8760108, 0.0415560],
                 [0.0556434, -0.2040259, 1.0572252]]

adobeRGBtoXYZ_D65 = [[0.5767309, 0.1855540, 0.1881852],
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

adobeRGBtoXYZ_D50 = [[0.6097559, 0.2052401, 0.1492240],
                     [0.3111242, 0.6256560, 0.0632197],
                     [0.0194811, 0.0608902, 0.7448387]]

XYZtoAdobeRGB_D50 = [[1.9624274, -0.6105343,-0.3413404],
                     [-0.9787684, 1.9161415, 0.0334540],
                     [0.0286869, -0.1406752, 1.3487655]]

ProPhotoXYZ_D50 = [[0.7976749, 0.1351917, 0.0313534],
                   [0.2880402, 0.7118741, 0.0000857],
                   [0.0000000, 0.0000000, 0.8252100]]

XYZtoProPhoto_D50 = [[1.3459433, -0.2556075, -0.0511118],
                     [-0.5445989, 1.5081673, 0.0205351],
                     [0.0000000, 0.0000000, 1.2118128]]

dicWPtoWSMatrix = { WPD65 : { 'sRGBtoXYZ'       : sRGBtoXYZ_D65,
                              'XYZtosRGB'       : XYZtosRGB_D65,
                              'adobeRGBtoXYZ'   : adobeRGBtoXYZ_D65,
                              'XYZtoAdobeRGB'   : XYZtoAdobeRGB_D65},
                    WPD50 : { 'sRGBtoXYZ'       : sRGBtoXYZ_D50,
                              'XYZtosRGB'       : XYZtosRGB_D50,
                              'adobeRGBtoXYZ'   : adobeRGBtoXYZ_D50,
                              'XYZtoAdobeRGB'   : XYZtoAdobeRGB_D50,
                              'ProPhotoXYZ'     : ProPhotoXYZ_D50,
                              'XYZtoProPhoto'   : XYZtoProPhoto_D50}}


def gammaDecode(normColor, gamma=2.2):
    return normColor ** (gamma)

def gammaEncode(normColor, gamma=2.2):
    return normColor ** (1.0/gamma)

def normalizeColor(color):
    assert (type(color)==int and 0 <= color <= 255)
    return color / 255.0

def denormalizeTo8bit(normValue):
    return min(255, max(0, int(normValue * 255)))

def RGBtoXYZ(ccInst, wp=None):
    w, h = ccInst.size[0], ccInst.size[1]
    oldWP = ccInst.getWP()
    newCCInst = ColorChannelInstance(w, h, None, wp=oldWP)
    for y in range(h):
        for x in range(w):
            R,G,B = ccInst[x,y]
            nR, nG, nB = normalizeColor(R), normalizeColor(G), normalizeColor(B)
            nLR, nLG, nLB = gammaDecode(nR), gammaDecode(nG), gammaDecode(nB)

            X = sum(map(lambda x,y: x*y, [nLR, nLG, nLB], dicWPtoWSMatrix[oldWP]['sRGBtoXYZ'][0]))
            Y = sum(map(lambda x,y: x*y, [nLR, nLG, nLB], dicWPtoWSMatrix[oldWP]['sRGBtoXYZ'][1]))
            Z = sum(map(lambda x,y: x*y, [nLR, nLG, nLB], dicWPtoWSMatrix[oldWP]['sRGBtoXYZ'][2]))
            newCCInst[x,y] = X,Y,Z
    return newCCInst

def XYZtoRGB(ccInst, wp=None):
    w, h = ccInst.size[0], ccInst.size[1]
    oldWP = ccInst.getWP()
    newCCInst = ColorChannelInstance(w, h, None)
    for y in range(h):
        for x in range(w):
            X,Y,Z = ccInst[x,y]

            nLR2 = sum(map(lambda x,y:x*y, [X, Y, Z], dicWPtoWSMatrix[oldWP]['XYZtosRGB'][0]))
            nLG2 = sum(map(lambda x,y:x*y, [X, Y, Z], dicWPtoWSMatrix[oldWP]['XYZtosRGB'][1]))
            nLB2 = sum(map(lambda x,y:x*y, [X, Y, Z], dicWPtoWSMatrix[oldWP]['XYZtosRGB'][2]))

            nGER = gammaEncode(nLR2)
            nGEG = gammaEncode(nLG2)
            nGEB = gammaEncode(nLB2)

            newCCInst[x,y] = denormalizeTo8bit(nGER), denormalizeTo8bit(nGEG), denormalizeTo8bit(nGEB)
    return newCCInst
