#import noisedefs

import gc
# add other imports
import math

gc.collect()
start_mem = gc.mem_free()
print( "Point 1 Available memory: {} bytes".format(start_mem) )

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
]




p1 = [
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
	209, 206, 248, 4, 56, 47, 226, 13, 144, 22, 11, 247, 70, 244, 48, 97
]

p2 = [
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
]

#arr = b'\x123\x43\x42\x01'

arr1 = bytes(p1)
arr2 = bytes(p2)
perm = p1 + p2

#print(len(perm))
#print(perm)



gc.collect()
end_mem = gc.mem_free()

print( "Point 2 Available memory: {} bytes".format(end_mem) )
print( "Code section 1-2 used {} bytes".format(start_mem - end_mem) )


f3 = 1.0/3.0
g3 = 1.0 / 6.0

class Simplex3D:
    def __init__(self):

        octaves = 1
        amplitude = 2
        frequency = 1
        persistance = 0.5
        scale = 1.0
        base = 0.0

        self.octaves = octaves
        self.frequency = frequency
        self.persistance = persistance
        self.scale = scale
        self.base = base

        if persistance ==1.0:
            self.scale = self.octaves * amplitude /2
            #print( float(octaves))
        else:
            self.scale = (1 - self.persistance) / (1 - pow( self.persistance, self.octaves)) * amplitude / 2.0
        self.base = base * amplitude / 2.0

    def show(self):
        print(self.scale)
        print(self.base)
        #print(grad)
        #print(perm)

    def generateNoise(self, xin, yin, zin):

        n0, n1, n2, n3 = None, None, None, None

        s = (xin + yin + zin) * f3; # Simple skew factor for 3D
        print("xin = " + str(xin))
        print("yin = " + str(yin))
        print("s = " + str(s))
        i = int(math.floor(xin + s));

        j = int(math.floor(yin + s));
        k = int(math.floor(zin + s));
        t = (i + j + k) * g3;
        print("i = " + str(i))

        x0 = i - t; # Unskew the cell origin back to (x,y,z) space
        y0 = j - t;
        z0 = k - t;
        x0 = xin - x0; # The x,y distances from the cell origin
        y0 = yin - y0;
        z0 = zin - z0;

        print(z0)

        i1, j1, k1 = None, None, None # Offsets for second corner of simplex in (i,j,k) coords
        i2, j2, k2 = None, None, None # Offsets for third corner of simplex in (i,j,k) coords
        if (x0 >= y0):
            if (y0 >= z0):
                i1 = 1
                j1 = 0
                k1 = 0
                i2 = 1
                j2 = 1
                k2 = 0 # X Y Z order
            elif (x0 >= z0):
                i1 = 1
                j1 = 0
                k1 = 0
                i2 = 1
                j2 = 0
                k2 = 1 # X Z Y order
            else:
                i1 = 0
                j1 = 0
                k1 = 1
                i2 = 1
                j2 = 0
                k2 = 1 # Z X Y order
        else: # x0<y0
            if (y0 < z0):
                i1 = 0
                j1 = 0
                k1 = 1
                i2 = 0
                j2 = 1
                k2 = 1 # Z Y X order
            elif (x0 < z0):
                i1 = 0
                j1 = 1
                k1 = 0
                i2 = 0
                j2 = 1
                k2 = 1 # Y Z X order
            else:
                i1 = 0
                j1 = 1
                k1 = 0
                i2 = 1
                j2 = 1
                k2 = 0 # Y X Z order
		
        # A step of (1,0,0) in (i,j,k) means a step of (1-c,-c,-c) in (x,y,z),
        # a step of (0,1,0) in (i,j,k) means a step of (-c,1-c,-c) in (x,y,z), and // a step of (0,0,1) in (i,j,k) means a step of (-c,-c,1-c) in (x,y,z), where // c = 1/6.
        x1 = x0 - i1 + g3 # Offsets for second corner in (x,y,z) coords
        y1 = y0 - j1 + g3
        z1 = z0 - k1 + g3
        x2 = x0 - i2 + 2.0 * g3 # Offsets for third corner in (x,y,z) coords
        y2 = y0 - j2 + 2.0 * g3
        z2 = z0 - k2 + 2.0 * g3
        x3 = x0 - 1.0 + 3.0 * g3 # Offsets for last corner in (x,y,z) coords
        y3 = y0 - 1.0 + 3.0 * g3
        z3 = z0 - 1.0 + 3.0 * g3



        ii = i & 255
        jj = j & 255
        kk = k & 255



        # Calculate the contribution from the three corners
        t0 = 0.5 - x0 * x0 - y0 * y0 - z0 * z0
        t1 = 0.5 - x1 * x1 - y1 * y1 - z1 * z1
        t2 = 0.5 - x2 * x2 - y2 * y2 - z2 * z2
        t3 = 0.5 - x3 * x3 - y3 * y3 - z3 * z3



        if (t0 < 0):
            n0 = 0.0
        else:
            gi0 = perm[ii + perm[jj + perm[kk]]] & 15
            t0 *= t0
            n0 = t0 * t0 * (grad[gi0][0] * x0 + grad[gi0][1] * y0 + grad[gi0][2] * z0)

        if (t1 < 0):
            n1 = 0.0
        else:
            gi1 = perm[ii + i1 + perm[jj + j1 + perm[kk + k1]]] & 15
            t1 *= t1
            n1 = t1 * t1 * (grad[gi1][0] * x1 + grad[gi1][1] * y1 + grad[gi1][2] * z1)

        if (t2 < 0):
            n2 = 0.0;
        else:
            gi2 = perm[ii + i2 + perm[jj + j2 + perm[kk + k2]]] & 15
            t2 *= t2
            n2 = t2 * t2 * (grad[gi2][0] * x2 + grad[gi2][1] * y2 + grad[gi2][2] * z2)
	
        if (t3 < 0):
            n3 = 0.0
        else:
            gi3 = perm[ii + 1 + perm[jj + 1 + perm[kk + 1]]] & 15
            t3 *= t3
            n3 = t3 * t3 * (grad[gi3][0] * x3 + grad[gi3][1] * y3 + grad[gi3][2] * z3)
	

        # Add contributions from each corner to get the final noise value.
        # The result is scaled to return values in the interval [-1,1].
        return( 32.0 * (n0 + n1 + n2 + n3))

    # Complexity in O(o)
    # with o the number of octaves
    def getNoise(self, x, y, z):
        noise = 0
        amp = 1.0
        for i in range (self.octaves):
            noise += self.generateNoise(x, y, z) * amp
            x *= self.frequency
            y *= self.frequency
            z *= self.frequency
            amp *= self.persistance
        return noise * self.scale + self.base
