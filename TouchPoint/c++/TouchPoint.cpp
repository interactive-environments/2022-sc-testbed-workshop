
#include <Arduino.h>
#include <Math.h>
#include "TouchPoint.h"


extern Stream * Console;  // NOTE: assumes this is set up to use either Serial or Telnet -- using Stream for flexibility

TouchPoint::TouchPoint(int _x, int _y, int _z, int _core, int _size, float _speed, int _lifespan, float _strength, float _fadeRatio) 
{
    x = _x;
    y = _y;
    z = _z;
    core = _core;
    size = _size;

    speed = _speed;
    lifespan = _lifespan;
    strength = _strength;
    fadeRatio =  _fadeRatio;
    
    initSize = size;
    initCore = core;
    initStrength = strength;

    live = true;
    born = millis();

    Console->printf("touch created with: %d, %d, %d, %d, %d, %f, %d, %f, %f \n",
    x, y, z, core, size, speed, lifespan, strength, fadeRatio);
    Console->printf("born is: %d \n", born);  
};

float TouchPoint::calculateTrigDistance(int x1, int y1, int z1, int x2, int y2, int z2) {
  // Calculate the trig distance between two 3D points
  float trigDistance =
      pow(pow((x2 - x1), 2.0) + pow((y2 - y1), 2.0) + pow((z2 - z1), 2.0), 0.5);

  return trigDistance;
}

float TouchPoint::donutWithCutoff(float x, int xMax, int xMin, float vMax, float vMin) {

    // like linearWithCutoff but also has a hole in the middle.  Donut width is original diameter, linear interp goes both ways
    int outerEdge = xMin;
    int outerCore = xMax;
    int innerEdge = xMin - initSize;                          // can be negative if no hole
    int innerCore = innerEdge + (outerEdge - outerCore);      // can be negative if no inner falloff (yet)

    if (x > (float)outerEdge || x < (float)innerEdge) {       // if it's beyond the outer boundary or within the donut hole
      return vMin;
    };

    if (x < (float)outerCore && x > (float)innerCore) {       // if it's within the inner boundary, on either side of the midpoint
      return vMax;
    };

    float gradient = -1.0;

    if (x > (float)outerCore) {                               // we are in outer gradient
      gradient = (vMin - vMax) / ((float)outerEdge - (float)outerCore);   // NOTE - DIV BY ZERO RISK??
      return vMax + gradient * (x - outerCore);
    } else {                                                  // we are in inner gradient
      gradient = (vMax) / ((float)innerCore - (float)innerEdge);          // NOTE - DIV BY ZERO RISK??
      return vMin + (gradient * (x - innerEdge));
    }

}

// old version, sphere not shell

float TouchPoint::linearWithCutoff(float x, int xMax, int xMin, float yMax, float yMin) {
  // Maps the input value (x) on a linear graph where:
  //  if x < xMax return yMax
  //  if x > xMin return yMin
  //  if xMax < x < xMin a proportional scaling between yMax and yMin
  if (x < (float)xMax) {
    return yMax;
  };
  if (x > (float)xMin) {
    return yMin;
  };

  float gradient = (yMin - yMax) / ((float)xMin - (float)xMax);
  return yMax + gradient * (x - xMax);
}


float TouchPoint::distanceInfluence(int x1, int y1, int z1, int x2, int y2, int z2,
                        int dInner, int dOuter) {
  // Compute the trig distance between point 1 and point 2 and output a float
  // between 0 and 1 inc If the distance is smaller than rInner then 1 If grater
  // than rOuter then 0 Between rOuter and rInner have a linear scale
  float rOuter = (float)dOuter / 2.0;
  float rInner = (float)dInner / 2.0;
  float trigDist = calculateTrigDistance(x1, y1, z1, x2, y2, z2);

  float returnValue = donutWithCutoff(trigDist, rInner, rOuter, 1.0, 0.0);
  return returnValue;
}




float TouchPoint::influenceOn(int x1, int y1, int z1) {
  
  float rOuter = (float)size / 2.0;
  float rInner = (float)core / 2.0;
  float trigDist = calculateTrigDistance(x1, y1, z1, x, y, z);

  float returnValue = strength * donutWithCutoff(trigDist, rInner, rOuter, 1.0, 0.0);

  return returnValue;
}

bool TouchPoint::update() {
    int age = millis() - born;
    int fadeAt = int(lifespan * fadeRatio);

    if(age > lifespan) {
      live = false;
      return(false);
    }

    if(age > fadeAt) {
      strength = initStrength * (1.0-(float(age - fadeAt)/float(lifespan - fadeAt)));
    }

    // now grow it according to its speed, in meters per second
    // age is in ms, so meters per second is equal to millimeters per milliseconds
    // size is diameter, so double the size increase
    size = initSize + (2 * speed * age);
    core = initCore + (2 * speed * age);

    return(true);
}


TouchPoint::~TouchPoint() 
{

};
