BYTE_ALIGN_INTEL    = 0x4949
BYTE_ALIGN_MOTOROLA = 0x4d4d

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
        self._file = None
        pass

    def __getcToOrd(self):
        if not self._file:
            assert False
        c = self._file.read(1)
        if c == '':
            return -1
        return ord(c)

    def __getLen2(self, order=BYTE_ALIGN_MOTOROLA):
        # 0x4d4d for MM / 0x4949 for II.
        lenLow = self.__getcToOrd()
        lenHigh = self.__getcToOrd()
        if order == BYTE_ALIGN_MOTOROLA:
            return lenLow << 8 | lenHigh
        else:
            return lenLow | lenHigh << 8

    def __getLen4(self, order=BYTE_ALIGN_MOTOROLA):
        # 0x4d4d for MM / 0x4949 for II.
        lenLL = self.__getcToOrd()
        lenLH = self.__getcToOrd()
        lenHL = self.__getcToOrd()
        lenHH = self.__getcToOrd()
        if order == BYTE_ALIGN_MOTOROLA:
            return lenLL << 24 | lenLH << 16 | lenHL << 8 | lenHH
        else:
            return lenLL | lenLH << 8 | lenHL << 16 | lenHH << 24

    def __parseBasicIFD(self):
        if not self._file:
            assert False
        pass

    def __parseAPP1(self, base, start, end):
        if not self._file:
            assert False

        self._file.seek(base)
        order = self.__getLen2()
        print "[APP1]...order=",hex(order)
        if order not in [BYTE_ALIGN_MOTOROLA, BYTE_ALIGN_INTEL]:
            print "[APP1]...order incorrect"
            assert False

        check = self.__getLen2(order)
        if check != 0x002a:
            assert False

        offsetToIFD = self.__getLen4(order)
        print "[APP1]...offsetToIFD =",hex(offsetToIFD)
        self._file.seek(base+offsetToIFD)

    def __parseXMP(self):
        if not self._file:
            assert False

    def parse(self, filePath):
        self._file = open(filePath)
        self._file.seek(0)
        first = self.__getcToOrd()
        marker = self.__getcToOrd()
        if (first != 0xff or marker != JPEG_SOI):
            assert False, "Not in JPEG format !!"

        while (marker):
            first = self.__getcToOrd()
            if first != 0xff or first < 0:
                break
            marker = self.__getcToOrd()
            print hex(first), hex(marker)
            len = self.__getLen2()
            curPos = self._file.tell()
            print "len= %d, curPos=%d"%(len,curPos)
            if marker in [JPEG_EOI, JPEG_SOS]:
                print "EOI or SOS ... exit parsing"
                break
            elif marker == JPEG_APP0:
                print "[APP0]..."
                pass # TBD
            elif marker == JPEG_APP1:
                print "[APP1]..."
                header = self._file.read(4)
                print "[APP1]...header=%s"%(header)
                if header.lower() == 'exif':
                    self.__parseAPP1(curPos+6, curPos, curPos+len-2)
                elif header.lower() == 'http':
                    pass

            elif marker == JPEG_APP2:
                print "[APP2]..."
                pass # TBD
            elif marker == JPEG_APP13:
                print "[APP13]"
                pass # TBD
            self._file.seek(curPos+len-2)

import os
fPath = "./images/tampa_AdobeRGB.jpg"
fullPath = os.path.abspath(fPath)

jpgParser = JPEGMetadataParser()
jpgParser.parse(fullPath)
