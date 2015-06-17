from ColorChannelInst import ColorChannelInstance

sRGBtoXYZ = [[0.4124564, 0.3575761, 0.1804375], 
                 [0.2126729, 0.7151522, 0.0721750],
                 [0.0193339, 0.1191920, 0.9503041]]
XYZtosRGB = [[3.2404542, -1.5371385, -0.4985314],
             [-0.9692660, 1.8760108, 0.0415560],
             [0.0556434, -0.2040259, 1.0572252]]


def gammaDecode(normColor, gamma=2.2):
    return normColor ** (gamma)

def gammaEncode(normColor, gamma=2.2):
    return normColor ** (1.0/gamma)

def normalizeColor(color):
    assert (type(color)==int and 0 <= color <= 255)
    return color / 255.0

def denormalizeTo8bit(normValue):
    return min(255, max(0, int(normValue * 255)))

def RGBtoXYZ(ccInst):
    w, h = ccInst.size[0], ccInst.size[1]
    newCCInst = ColorChannelInstance(w, h, None)
    for y in range(h):
        for x in range(w):
            R,G,B = ccInst[x,y]
            nR, nG, nB = normalizeColor(R), normalizeColor(G), normalizeColor(B)
            nLR, nLG, nLB = gammaDecode(nR), gammaDecode(nG), gammaDecode(nB)

            X = sum(map(lambda x,y: x*y, [nLR, nLG, nLB], sRGBtoXYZ[0]))
            Y = sum(map(lambda x,y: x*y, [nLR, nLG, nLB], sRGBtoXYZ[1]))
            Z = sum(map(lambda x,y: x*y, [nLR, nLG, nLB], sRGBtoXYZ[2]))
            newCCInst[x,y] = X,Y,Z
    return newCCInst

def XYZtoRGB(ccInst):
    w, h = ccInst.size[0], ccInst.size[1]
    newCCInst = ColorChannelInstance(w, h, None)
    for y in range(h):
        for x in range(w):
            X,Y,Z = ccInst[x,y]

            nLR2 = sum(map(lambda x,y:x*y, [X, Y, Z], XYZtosRGB[0]))
            nLG2 = sum(map(lambda x,y:x*y, [X, Y, Z], XYZtosRGB[1]))
            nLB2 = sum(map(lambda x,y:x*y, [X, Y, Z], XYZtosRGB[2]))

            nGER = gammaEncode(nLR2)
            nGEG = gammaEncode(nLG2)
            nGEB = gammaEncode(nLB2)

            newCCInst[x,y] = denormalizeTo8bit(nGER), denormalizeTo8bit(nGEG), denormalizeTo8bit(nGEB) 
    return newCCInst
