
# Start Of Frame N
# N indicates the compression process, only SOF0~SOF2 are commonly used.

# Nondifferential Huffman-coding frames
JPEG_SOF0   = 0xc0 # Baseline DCT
JPEG_SOF1   = 0xc1 # Extended sequential DCT
JPEG_SOF2   = 0xc2 # Progressive DCT
JPEG_SOF3   = 0xc3 # Lossless (sequential)
# Differential Huffman-coding frames
JPEG_SOF5   = 0xc5 # Differential sequential DCT
JPEG_SOF6   = 0xc6 # Differential progressive DCT
JPEG_SOF7   = 0xc7 # Differential lossless
# Nodifferential arithmetic-coding frames
JPEG_SOF9   = 0xc9 # Extended sequential DCT
JPEG_SOF10  = 0xca # Progressive DCT
JPEG_SOF11  = 0xcb # Lossless (sequential)
# Differential arithmetic-coding frames
JPEG_SOF13  = 0xcd # Differential sequential DCT
JPEG_SOF14  = 0xce # Differential progressive DCT
JPEG_SOF15  = 0xcf # Differential lossless

JPEG_SOI    = 0xd8 # Start Of Image
JPEG_EOI    = 0xd9 # End Of Image
JPEG_SOS    = 0xda # Start Of Scan
JPEG_APP0   = 0xe0 # Jfif marker
JPEG_APP1   = 0xe1 # Exif marker
JPEG_APP2   = 0xe2
JPEG_COM    = 0xfe # Comment
JPEG_DQT    = 0xdb # Define quantization table(s)
JPEG_DHT    = 0xc4 # Define Huffman table(s)
JPEG_DRI    = 0xdd # Define restart interval
JPEG_APP13  = 0xed

class JPEGMetadataParser:
    def __init__(self):
        pass

    def parse(self, filePath):
        def getcToOrd(fileObj):
            c = fileObj.read(1)
            if c == '':
                return -1
            return ord(c)
        def getLen(fObj, order=0x4d4d): # 0x4d4d for MM / 0x4949 for II.
            lenLow = getcToOrd(fObj)
            lenHigh = getcToOrd(fObj)
            if order == 0x4d4d:
                return lenLow << 8 | lenHigh
            else:
                return lenLow | lenHigh << 8

        fObj = open(filePath)
        fObj.seek(0)
        first = getcToOrd(fObj)
        marker = getcToOrd(fObj)
        if (first != 0xff or marker != JPEG_SOI):
            assert False, "Not in JPEG format !!"

        while (marker):
            first = getcToOrd(fObj)
            if first != 0xff or first < 0:
                break
            marker = getcToOrd(fObj)
            print hex(first), hex(marker)
            len = getLen(fObj)
            curPos = fObj.tell()
            print "len= %d, curPos=%d"%(len,curPos)
            if marker in [JPEG_EOI, JPEG_SOS]:
                print "EOI or SOS ... exit parsing"
                break
            elif marker == JPEG_APP0:
                print "app0"
                pass # TBD
            elif marker == JPEG_APP1:
                print "app1"
                pass # TBD
            elif marker == JPEG_APP2:
                print "app2"
                pass # TBD
            elif marker == JPEG_APP13:
                print "app13"
                pass # TBD
            fObj.seek(curPos+len-2)

import os
fPath = "./images/tampa_AdobeRGB.jpg"
fullPath = os.path.abspath(fPath)

jpgParser = JPEGMetadataParser()
jpgParser.parse(fullPath)
