__kernel void cmm(unsigned int pixelCount,
                  __global unsigned char* in,
                  __global unsigned char* out)
{
    unsigned int gid = get_global_id(0);
    if (gid >= pixelCount)
        return;
    out[gid] = in[gid];
}