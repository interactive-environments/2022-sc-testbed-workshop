#ifndef SIMPLERSIMPLEXNOISE_H
#define SIMPLERSIMPLEXNOISE_H


#include "Arduino.h"

/**
 * @classdesc 3-dimensional Simplex Noise
 * @class
 *
 * @author Brice Chevalier
 *
 *  PORTED FROM JAVASCRIPT BY MATT GORBET OCT 2022
 */


class Simplex3D 
{

    public:

    Simplex3D();
    ~Simplex3D();

    double getNoise(double x, double y, double z);
    double generateNoise(double xin, double yin, double zin);

    private:

    int octaves = 1;
    int amplitude = 2;
    int frequency = 1;
    float persistance = 0.5;  // 0.0 to 1.0 
    float scale = 1.0;
    float base = 0;

    float f3 = 1.0 / 3.0;
    float g3 = 1.0 / 6.0;





    // NOTE MATRICES ARE IN SEPARATE "NOISEDEFS.H" FUNCTION SO THEY WOULD COMPILE (AS GLOBAL)

};

#endif
