/**
 * @classdesc 3-dimensional Simplex Noise
 * @class
 *
 * @author Brice Chevalier
 *
 * @param {object} params
 * @param {number} params.octaves
 * @param {number} params.amplitude
 * @param {number} params.frequency
 * @param {number} params.persistance
 * @param {number} params.base
 */

class Simplex3D {


f3 = 1.0 / 3.0;
g3 = 1.0 / 6.0;

grad = [
	[1, 1, 0],
	[-1, 1, 0],
	[1, -1, 0],
	[-1, -1, 0],
	[1, 0, 1],
	[-1, 0, 1],
	[1, 0, -1],
	[-1, 0, -1],
	[0, 1, 1],
	[0, -1, 1],
	[0, 1, -1],
	[0, -1, -1],
	[-1, 1, 1],
	[1, -1, 1],
	[1, 1, -1],
	[0, 0, 0]
];

// this.permutation table
perm = [
	182, 235, 131, 26, 88, 132, 100, 117, 202, 176, 10, 19, 83, 243, 75, 52,
	252, 194, 32, 30, 72, 15, 124, 53, 236, 183, 121, 103, 175, 39, 253, 120,
	166, 33, 237, 141, 99, 180, 18, 143, 69, 136, 173, 21, 210, 189, 16, 142,
	190, 130, 109, 186, 104, 80, 62, 51, 165, 25, 122, 119, 42, 219, 146, 61,
	149, 177, 54, 158, 27, 170, 60, 201, 159, 193, 203, 58, 154, 222, 78, 138,
	220, 41, 98, 14, 156, 31, 29, 246, 81, 181, 40, 161, 192, 227, 35, 241,
	135, 150, 89, 68, 134, 114, 230, 123, 187, 179, 67, 217, 71, 218, 7, 148,
	228, 251, 93, 8, 140, 125, 73, 37, 82, 28, 112, 24, 174, 118, 232, 137,
	191, 133, 147, 245, 6, 172, 95, 113, 185, 205, 254, 116, 55, 198, 57, 152,
	128, 233, 74, 225, 34, 223, 79, 111, 215, 85, 200, 9, 242, 12, 167, 44,
	20, 110, 107, 126, 86, 231, 234, 76, 207, 102, 214, 238, 221, 145, 213, 64,
	197, 38, 168, 157, 87, 92, 255, 212, 49, 196, 240, 90, 63, 0, 77, 94,
	1, 108, 91, 17, 224, 188, 153, 250, 249, 199, 127, 59, 46, 184, 36, 43,
	209, 206, 248, 4, 56, 47, 226, 13, 144, 22, 11, 247, 70, 244, 48, 97,
	151, 195, 96, 101, 45, 66, 239, 178, 171, 160, 84, 65, 23, 3, 211, 162,
	163, 50, 105, 129, 155, 169, 115, 5, 106, 2, 208, 204, 139, 229, 164, 216,
	182, 235, 131, 26, 88, 132, 100, 117, 202, 176, 10, 19, 83, 243, 75, 52,
	252, 194, 32, 30, 72, 15, 124, 53, 236, 183, 121, 103, 175, 39, 253, 120,
	166, 33, 237, 141, 99, 180, 18, 143, 69, 136, 173, 21, 210, 189, 16, 142,
	190, 130, 109, 186, 104, 80, 62, 51, 165, 25, 122, 119, 42, 219, 146, 61,
	149, 177, 54, 158, 27, 170, 60, 201, 159, 193, 203, 58, 154, 222, 78, 138,
	220, 41, 98, 14, 156, 31, 29, 246, 81, 181, 40, 161, 192, 227, 35, 241,
	135, 150, 89, 68, 134, 114, 230, 123, 187, 179, 67, 217, 71, 218, 7, 148,
	228, 251, 93, 8, 140, 125, 73, 37, 82, 28, 112, 24, 174, 118, 232, 137,
	191, 133, 147, 245, 6, 172, 95, 113, 185, 205, 254, 116, 55, 198, 57, 152,
	128, 233, 74, 225, 34, 223, 79, 111, 215, 85, 200, 9, 242, 12, 167, 44,
	20, 110, 107, 126, 86, 231, 234, 76, 207, 102, 214, 238, 221, 145, 213, 64,
	197, 38, 168, 157, 87, 92, 255, 212, 49, 196, 240, 90, 63, 0, 77, 94,
	1, 108, 91, 17, 224, 188, 153, 250, 249, 199, 127, 59, 46, 184, 36, 43,
	209, 206, 248, 4, 56, 47, 226, 13, 144, 22, 11, 247, 70, 244, 48, 97,
	151, 195, 96, 101, 45, 66, 239, 178, 171, 160, 84, 65, 23, 3, 211, 162,
	163, 50, 105, 129, 155, 169, 115, 5, 106, 2, 208, 204, 139, 229, 164, 216
];


constructor(params) {

	// NOTE for our app, none of this matters - we call the generateNoise function directly -mg Oct 2022

	params = params || {};
	this.octaves = !params.octaves ? 1 : params.octaves;
	this.amplitude = !params.amplitude ? 2 : params.amplitude;
	this.frequency = !params.frequency ? 1: params.frequency;
	this.persistance = !params.persistance ? 0.5 : Math.min(Math.max(params.persistance, 0), 1);

	// The scale is used to put the noise value in the interval [-amplitude / 2; amplitude / 2]
	this.scale = (this.persistance === 1) ? this.octaves * this.amplitude / 2 : (1 - this.persistance) / (1 - Math.pow(this.persistance, this.octaves)) * this.amplitude / 2;

	// The base is used to put the noise value in the interval [base; amplitude + base]
	this.base = (params.base || 0) + this.amplitude / 2;
}


generateNoise (xin, yin, zin) {
	var n0, n1, n2, n3; // Noise contributions from the four corners

	// Skew the input space to determine which simplex cell we're in
	var s = (xin + yin + zin) * this.f3; // Simple skew factor for 3D
	var i = Math.floor(xin + s);
	var j = Math.floor(yin + s);
	var k = Math.floor(zin + s);
	var t = (i + j + k) * this.g3;

	var x0 = i - t; // Unskew the cell origin back to (x,y,z) space
	var y0 = j - t;
	var z0 = k - t;
	x0 = xin - x0; // The x,y distances from the cell origin
	y0 = yin - y0;
	z0 = zin - z0;

	// For the 3D case, the simplex shape is a slightly irregular tetrahedron. // Determine which simplex we are in.
	var i1, j1, k1; // Offsets for second corner of simplex in (i,j,k) coords
	var i2, j2, k2; // Offsets for third corner of simplex in (i,j,k) coords
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
	var x1 = x0 - i1 + this.g3; // Offsets for second corner in (x,y,z) coords
	var y1 = y0 - j1 + this.g3;
	var z1 = z0 - k1 + this.g3;
	var x2 = x0 - i2 + 2.0 * this.g3; // Offsets for third corner in (x,y,z) coords
	var y2 = y0 - j2 + 2.0 * this.g3;
	var z2 = z0 - k2 + 2.0 * this.g3;
	var x3 = x0 - 1.0 + 3.0 * this.g3; // Offsets for last corner in (x,y,z) coords
	var y3 = y0 - 1.0 + 3.0 * this.g3;
	var z3 = z0 - 1.0 + 3.0 * this.g3;

	// Work out the hashed this.gradient indices of the three simplex corners
	var ii = i & 255;
	var jj = j & 255;
	var kk = k & 255;

	// Calculate the contribution from the three corners
	var t0 = 0.5 - x0 * x0 - y0 * y0 - z0 * z0;
	var t1 = 0.5 - x1 * x1 - y1 * y1 - z1 * z1;
	var t2 = 0.5 - x2 * x2 - y2 * y2 - z2 * z2;
	var t3 = 0.5 - x3 * x3 - y3 * y3 - z3 * z3;

	if (t0 < 0) {
		n0 = 0.0;
	} else {
		var gi0 = this.perm[ii + this.perm[jj + this.perm[kk]]] & 15;
		t0 *= t0;
		n0 = t0 * t0 * (this.grad[gi0][0] * x0 + this.grad[gi0][1] * y0 + this.grad[gi0][2] * z0);
	}

	if (t1 < 0) {
		n1 = 0.0;
	} else {
		var gi1 = this.perm[ii + i1 + this.perm[jj + j1 + this.perm[kk + k1]]] & 15;
		t1 *= t1;
		n1 = t1 * t1 * (this.grad[gi1][0] * x1 + this.grad[gi1][1] * y1 + this.grad[gi1][2] * z1);
	}

	if (t2 < 0) {
		n2 = 0.0;
	} else {
		var gi2 = this.perm[ii + i2 + this.perm[jj + j2 + this.perm[kk + k2]]] & 15;
		t2 *= t2;
		n2 = t2 * t2 * (this.grad[gi2][0] * x2 + this.grad[gi2][1] * y2 + this.grad[gi2][2] * z2);
	}

	if (t3 < 0) {
		n3 = 0.0;
	} else {
		var gi3 = this.perm[ii + 1 + this.perm[jj + 1 + this.perm[kk + 1]]] & 15;
		t3 *= t3;
		n3 = t3 * t3 * (this.grad[gi3][0] * x3 + this.grad[gi3][1] * y3 + this.grad[gi3][2] * z3);
	}

	// Add contributions from each corner to get the final noise value.
	// The result is scaled to return values in the interval [-1,1].
	return 32.0 * (n0 + n1 + n2 + n3);
};


/// NOTE - for our app, we don't use the fancy scaling and shifting and octaves features - we call the above function, not getNoise. - mg Oct 2022

// Complexity in O(o)
// with o the number of octaves
getNoise(x, y, z) {
	var noise = 0;
	var amp = 1.0;

	for (var o = 0; o < this.octaves; o += 1) {
		noise += this.generateNoise(x, y, z) * amp;
		x *= this.frequency;
		y *= this.frequency;
		z *= this.frequency;
		amp *= this.persistance;
	}

	return noise * this.scale + this.base;  
};


}