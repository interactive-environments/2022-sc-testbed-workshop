
// code snippet for touchPoint class

// to use: instantiate touch with constructor, call update() on each loop, 
//         check influence upon any point with influenceOn().

// This version assumes variables set elsewhere (GUI) as follows, 
// but could send any of these to constructor as well if desired

var tpnt = {

    settings: {
        coreRatio : 0.5,     // 'softness' of touch - core vs. full size (0.0 - 1.0)
        size      : 600,     // initial diameter, and width of expanding shell, in mm
        strength  : 0.8,     // strength of touch (0.0 - 1.0)
        speed     : 0.2,     // speed of expansion in m/s (mm/millis)
        lifespan  : 2000,    // lifespan of effect
        fadeRatio : 0.7,     // percentage of lifespan before fade begins (0.0 - 1.0)
        defaultZ  : 2800     // hack - all input defaults to a plane at 2.8m
    }

}

/********* CLASS TOUCHPOINT **********/

class touchPoint {

    constructor(_x, _y) {
  
      this.x = _x;
      this.y = _y;
      this.z = tpnt.settings.defaultZ;
  
      this.coreRatio = tpnt.settings.coreRatio;
      this.size = tpnt.settings.size;
      this.strength = tpnt.settings.strength;
      this.speed = tpnt.settings.speed;
      this.lifespan = tpnt.settings.lifespan;
      this.fadeRatio = tpnt.settings.fadeRatio;
      
      this.initSize = this.size;
      this.core = this.coreRatio * this.size;
      this.initCore = this.core;
      this.initStrength = this.strength;
  
      this.live = true;
      this.born = millis();
      
    }
  
    update() {
  
      var age = millis() - this.born;
      var fadeAt = int(float(this.lifespan) * this.fadeRatio);
  
      if(age > this.lifespan) {
        this.live = false;
        return(false);
      }
      
      if(age > fadeAt) {
        this.strength = this.initStrength * (1.0-(float(age - fadeAt)/float(this.lifespan - fadeAt)));
      }
  
      // now grow it according to its speed, in meters per second
      // age is in ms, so meters per second is equal to millimeters per milliseconds
      // size is diameter, so double the size increase
      this.size = this.initSize + (2 * this.speed * age);
      this.core = this.initCore + (2 * this.speed * age);
  
      return(true);
  
    }
  
    influenceOn(x1, y1, z1) {
    
    var  rOuter = this.size / 2.0;
    var  rInner = this.core / 2.0;
    var  trigDist = this.calculateTrigDistance(x1, y1, z1, this.x, this.y, this.z);
  
    var  returnValue = this.strength * this.donutWithCutoff(trigDist, rInner, rOuter, 1.0, 0.0);
    return returnValue;
  
    }
  
    calculateTrigDistance(x1, y1, z1, x2, y2, z2) {
    // Calculate the trig distance between two 3D points
      var trigDistance = pow(pow((x2 - x1), 2.0) + pow((y2 - y1), 2.0) + pow((z2 - z1), 2.0), 0.5);
      return trigDistance;
    }
  
    donutWithCutoff(x, xMax, xMin, vMax, vMin) {
  
      // like linearWithCutoff but also has a hole in the middle.  Donut width is original diameter, linear interp goes both ways
      var outerEdge = xMin;
      var outerCore = xMax;
      var innerEdge = xMin - this.initSize;                   // can be negative if no hole
      var innerCore = innerEdge + (outerEdge - outerCore);    // can be negative if no inner falloff (yet)
  
      if (x > outerEdge || x < innerEdge) {       // if it's beyond the outer boundary or within the donut hole
        return vMin;
      };
  
      if (x < outerCore && x > innerCore) {   // if it's within the inner boundary, on either side of the midpoint
        return vMax;
      };
  
      var gradient = -1.0;
  
      if (x > outerCore) {                                     // we are in outer gradient
        gradient = (vMin - vMax) / (outerEdge - outerCore);
        return vMax + gradient * (x - outerCore);
      } else {                                                 // we are in inner gradient
        gradient = (vMax) / (innerCore - innerEdge);
        return vMin + (gradient * (x - innerEdge));
      }
  
    }

    // old version, sphere, not shell

    linearWithCutoff(x, xMax, xMin, yMax, yMin) {
        // Maps the input value (x) on a linear graph where:
        //  if x < xMax return yMax
        //  if x > xMin return yMin
        //  if xMax < x < xMin a proportional scaling between yMax and yMin
        if (x < xMax) {
          return yMax;
        };
        if (x > xMin) {
          return yMin;
        };
    
        var gradient = (yMin - yMax) / (xMin - xMax);
        return yMax + gradient * (x - xMax);
    }
      
}
  
  
  
