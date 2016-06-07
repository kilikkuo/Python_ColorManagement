# Python_ColorManagement

GOAL : Make a color management system in python and improve performance by
       PyOpenCL

Stage

1. To implement RGB_XYZ color space transformation via python
 - Need to obtain image metadata.
  [options] 1) python module "exifread".
            2) python module "PIL".
            3) cross-platform executable "exiftool" under ./Image-ExifTool-10.15/
               Downloaded from http://www.sno.phy.queensu.ca/~phil/exiftool/index.html
            4) a JPEGMetadataParser via python
               https://github.com/kilikkuo/JPEGMetadataParser

 - Need to define all required transformation matrics.
   http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html

 - See RGB_XYZ.py / ColorChannelInst.py / EXIF_ColorProfileParser.py

2. Implement algorithm of stage 1 via OpenCL kernel function.
 - See cmm.json / temp_algorithm.c

3. Bridge 2 via kernel-mapper (A tool to simplify the use of PyOpenCL)
 - https://goo.gl/nSyWz8

# Images used under ./images/ are copied & modified (for programming test) from
 https://www.flickr.com/photos/boston_public_library/8102625287/in/photostream/
 http://dev.exiv2.org/attachments/download/820/Reagan.jpg
 http://www.myriad-online.com/cgi-bin/bbs/YaBB.pl?board=galerie;action=display;num=1141256379

# Prepare dependences after clone
 $> git submodule init
 $> git submodule update

# Usage
e.g.
 1) $> python demo.py --help
 2) $> python demo.py -i PATH_TO_INPUT -ocs sRGB -owp D65
 3) $> python demo.py -i PATH_TO_INPUT -ocs ProPhotoRGB -owp D50 -o PATH_TO_OUTPUT
