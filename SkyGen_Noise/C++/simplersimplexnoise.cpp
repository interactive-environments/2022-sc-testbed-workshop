/**
 * @classdesc 3-dimensional Simplex Noise
 * @class
 *
 * @author Brice Chevalier
 *
 *  PORTED FROM JAVASCRIPT BY MATT GORBET OCT 2022
 */

#include "simplersimplexnoise.h"

extern int8_t grad[16][3];
extern uint8_t perm[512];


Simplex3D::Simplex3D() {


	//params = params || {};

    // SET IN .h file - mg

	// octaves = !params.octaves ? 1 : params.octaves;
	// amplitude = !params.amplitude ? 1 : params.amplitude;
	// frequency = !params.frequency ? 1 : params.frequency;
	// persistance = !params.persistance ? 0.5 : min(max(params.persistance, 0), 1);

	// The scale is used to put the noise value in the interval [-amplitude / 2; amplitude / 2]
	scale = (persistance == 1.) ? octaves * amplitude / 2 : (1 - persistance) / (1 - pow(persistance, octaves)) * amplitude / 2.;

	// The base is used to put the noise value in the interval [base; amplitude + base]
	base = base + amplitude / 2.;
 

}

Simplex3D::~Simplex3D() {
  
}

double Simplex3D::generateNoise (double xin, double yin, double zin) {
	double n0, n1, n2, n3; // Noise contributions from the four corners

	// Skew the input space to determine which simplex cell we're in
	double s = (xin + yin + zin) * f3; // Simple skew factor for 3D
	int i = static_cast<int>(floor(xin + s));
	int j = static_cast<int>(floor(yin + s));
	int k = static_cast<int>(floor(zin + s));
	double t = (i + j + k) * g3;

	double x0 = i - t; // Unskew the cell origin back to (x,y,z) space
	double y0 = j - t;
	double z0 = k - t;
	x0 = xin - x0; // The x,y distances from the cell origin
	y0 = yin - y0;
	z0 = zin - z0;

	// For the 3D case, the simplex shape is a slightly irregular tetrahedron. // Determine which simplex we are in.
	int i1, j1, k1; // Offsets for second corner of simplex in (i,j,k) coords
	int i2, j2, k2; // Offsets for third corner of simplex in (i,j,k) coords
	if (x0 >= y0) {
		if (y0 >= z0) {
			i1 = 1;
			j1 = 0;
			k1 = 0;
			i2 = 1;
			j2 = 1;
			k2 = 0; // X Y Z order
		} else if (x0 >= z0) {
			i1 = 1;
			j1 = 0;
			k1 = 0;
			i2 = 1;
			j2 = 0;
			k2 = 1; // X Z Y order
		} else {
			i1 = 0;
			j1 = 0;
			k1 = 1;
			i2 = 1;
			j2 = 0;
			k2 = 1; // Z X Y order
		}
	} else { // x0<y0
		if (y0 < z0) {
			i1 = 0;
			j1 = 0;
			k1 = 1;
			i2 = 0;
			j2 = 1;
			k2 = 1; // Z Y X order
		} else if (x0 < z0) {
			i1 = 0;
			j1 = 1;
			k1 = 0;
			i2 = 0;
			j2 = 1;
			k2 = 1; // Y Z X order
		} else {
			i1 = 0;
			j1 = 1;
			k1 = 0;
			i2 = 1;
			j2 = 1;
			k2 = 0; // Y X Z order
		}
	}

	// A step of (1,0,0) in (i,j,k) means a step of (1-c,-c,-c) in (x,y,z),
	// a step of (0,1,0) in (i,j,k) means a step of (-c,1-c,-c) in (x,y,z), and // a step of (0,0,1) in (i,j,k) means a step of (-c,-c,1-c) in (x,y,z), where // c = 1/6.
	double x1 = x0 - i1 + g3; // Offsets for second corner in (x,y,z) coords
	double y1 = y0 - j1 + g3;
	double z1 = z0 - k1 + g3;
	double x2 = x0 - i2 + 2.0 * g3; // Offsets for third corner in (x,y,z) coords
	double y2 = y0 - j2 + 2.0 * g3;
	double z2 = z0 - k2 + 2.0 * g3;
	double x3 = x0 - 1.0 + 3.0 * g3; // Offsets for last corner in (x,y,z) coords
	double y3 = y0 - 1.0 + 3.0 * g3;
	double z3 = z0 - 1.0 + 3.0 * g3;

	// Work out the hashed gradient indices of the three simplex corners
	int ii = i & 255;
	int jj = j & 255;
	int kk = k & 255;

	// Calculate the contribution from the three corners
	double t0 = 0.5 - x0 * x0 - y0 * y0 - z0 * z0;
	double t1 = 0.5 - x1 * x1 - y1 * y1 - z1 * z1;
	double t2 = 0.5 - x2 * x2 - y2 * y2 - z2 * z2;
	double t3 = 0.5 - x3 * x3 - y3 * y3 - z3 * z3;

	if (t0 < 0) {
		n0 = 0.0;
	} else {
		int32_t gi0 = perm[ii + perm[jj + perm[kk]]] & 15;
		t0 *= t0;
		n0 = t0 * t0 * (grad[gi0][0] * x0 + grad[gi0][1] * y0 + grad[gi0][2] * z0);
	}

	if (t1 < 0) {
		n1 = 0.0;
	} else {
		int32_t gi1 = perm[ii + i1 + perm[jj + j1 + perm[kk + k1]]] & 15;
		t1 *= t1;
		n1 = t1 * t1 * (grad[gi1][0] * x1 + grad[gi1][1] * y1 + grad[gi1][2] * z1);
	}

	if (t2 < 0) {
		n2 = 0.0;
	} else {
		int32_t gi2 = perm[ii + i2 + perm[jj + j2 + perm[kk + k2]]] & 15;
		t2 *= t2;
		n2 = t2 * t2 * (grad[gi2][0] * x2 + grad[gi2][1] * y2 + grad[gi2][2] * z2);
	}

	if (t3 < 0) {
		n3 = 0.0;
	} else {
		int32_t gi3 = perm[ii + 1 + perm[jj + 1 + perm[kk + 1]]] & 15;
		t3 *= t3;
		n3 = t3 * t3 * (grad[gi3][0] * x3 + grad[gi3][1] * y3 + grad[gi3][2] * z3);
	}

	// Add contributions from each corner to get the final noise value.
	// The result is scaled to return values in the interval [-1,1].
	return 32.0 * (n0 + n1 + n2 + n3);
};

// Complexity in O(o)
// with o the number of octaves
  double Simplex3D::getNoise(double x, double y, double z) {
	double noise = 0;
	double amp = 1.0;

	for (int o = 0; o < octaves; o += 1) {
		noise += generateNoise(x, y, z) * amp;
		x *= frequency;
		y *= frequency;
		z *= frequency;
		amp *= persistance;
	}

	return noise * scale + base;
};
