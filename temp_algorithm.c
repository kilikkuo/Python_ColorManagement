#include "color_management_structs.h"

__kernel void rgb_to_yuv(int aWidth,
                         int aHeight,
                         __global RGBPixel* aBufferIn,
                         __global YUVPixel* aBufferOut) {
  // Please implement your kernel code here.
  unsigned int gid_x = get_global_id(0);
  unsigned int gid_y = get_global_id(1);

  unsigned int index = gid_x + gid_y * aWidth;

  unsigned char r = aBufferIn[index].red;
  unsigned char g = aBufferIn[index].green;
  unsigned char b = aBufferIn[index].blue;

  float y = 0.299f*r + 0.587f*g + 0.114f*b;
  float u = -0.147f*r - 0.289f*g + 0.436f*b;
  float v = 0.615f*r - 0.515f*g - 0.100f*b;

  aBufferOut[index].y = y;
  aBufferOut[index].u = u;
  aBufferOut[index].v = v;
}

__kernel void yuv_to_rgb(int aWidth,
                         int aHeight,
                         __global YUVPixel* aBufferIn,
                         __global RGBPixel* aBufferOut) {
  // Please implement your kernel code here.
  unsigned int gid_x = get_global_id(0);
  unsigned int gid_y = get_global_id(1);

  unsigned int index = gid_x + gid_y * aWidth;

  float y = aBufferIn[index].y;
  float u = aBufferIn[index].u;
  float v = aBufferIn[index].v;
  aBufferOut[index].red  = (unsigned char)fmin(255.0f, fmax(0.0f, y + 1.14f*v));
  aBufferOut[index].green = (unsigned char)fmin(255.0f, fmax(0.0f, y - 0.39f*u - 0.58f*v));
  aBufferOut[index].blue = (unsigned char)fmin(255.0f, fmax(0.0f, y + 2.03f*u));
}

