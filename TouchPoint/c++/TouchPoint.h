#pragma once

#define DEFAULT_TOUCH_SPEED     0.2
#define DEFAULT_TOUCH_LIFESPAN  2000
#define DEFAULT_TOUCH_STRENGTH  0.8
#define DEFAULT_TOUCH_FADERATIO 0.7


class TouchPoint {

private:
float calculateTrigDistance(int x1, int y1, int z1, int x2, int y2, int z2);
float linearWithCutoff(float x, int xMax, int xMin, float yMax, float yMin);
float donutWithCutoff(float x, int xMax, int xMin, float vMax, float vMin);

public:

    int x;
    int y;
    int z;
    int core;
    int size;
    int initSize;
    int initCore;
    int lifespan = 2.0;
    float speed;

    long born;

    float strength = 1.0;
    float initStrength = 1.0;
    float fadeRatio = 0.8;  // 0.0 - 1.0 -- when does its strenght start fading?

    bool live = false;
   
    TouchPoint(int x, int y, int z, int core, int size, float speed, int lifespan, float strength, float fadeRatio);

    ~TouchPoint();

    float distanceInfluence(int x1, int y1, int z1, int x2, int y2, int z2, int dInner, int dOuter);
    float influenceOn(int x1, int y1, int z1);
    bool update();

};
