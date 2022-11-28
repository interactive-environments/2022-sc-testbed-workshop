public class Simplex3D {
  double f3 = 1.0/3.0;
  double g3 = 1.0/6.0;
  int[][] grad = {{1, 1, 0},
    {-1, 1, 0},
    {1, -1, 0},
    {-1, -1, 0},
    {1, 0, 1},
    {-1, 0, 1},
    {1, 0, -1},
    {-1, 0, -1},
    {0, 1, 1},
    {0, -1, 1},
    {0, 1, -1},
    {0, -1, -1},
    {-1, 1, 1},
    {1, -1, 1},
    {1, 1, -1},
    {0, 0, 0}};

  int[] perm = {
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
  };

  int octaves;
  int amplitude;
  int frequency;
  float persistence;
  double scale;
  int base;

  public Simplex3D() {
    this.octaves = 1;
    this.amplitude = 2;
    this.frequency = 1;
    this.persistence = 0.5;
    this.base = 0;

    this.scale = (this.persistence == 1) ?
      this.octaves * this.amplitude / 2 : (1- this.persistence) /  (1 - Math.pow(this.persistence, this.octaves)) * this.amplitude / 2;

    this.base = (this.base | 0) * this.amplitude / 2;
  }

  double generateNoise(double xin, double yin, double zin) {
    double n0, n1, n2, n3;
    double s = (xin + yin + zin) * f3;
    int i = (int)Math.floor((xin + s));
    int j = (int)Math.floor((yin + s));
    int k = (int)Math.floor((zin + s));
    double t = (i + j + k) * g3;

    double x0 = i - t;
    double y0 = j - t;
    double z0 = k - t;

    x0 = xin - x0;
    y0 = yin - y0;
    z0 = zin - z0;

    int i1, j1, k1;
    int i2, j2, k2;
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
    double x1 = x0 - i1 + this.g3; // Offsets for second corner in (x,y,z) coords
    double y1 = y0 - j1 + this.g3;
    double z1 = z0 - k1 + this.g3;
    double x2 = x0 - i2 + 2.0 * this.g3; // Offsets for third corner in (x,y,z) coords
    double y2 = y0 - j2 + 2.0 * this.g3;
    double z2 = z0 - k2 + 2.0 * this.g3;
    double x3 = x0 - 1.0 + 3.0 * this.g3; // Offsets for last corner in (x,y,z) coords
    double y3 = y0 - 1.0 + 3.0 * this.g3;
    double z3 = z0 - 1.0 + 3.0 * this.g3;

    int ii = i & 255;
    int jj = j & 255;
    int kk = k & 255;

    double t0 = 0.5 - x0 * x0 - y0 * y0 - z0 * z0;
    double t1 = 0.5 - x1 * x1 - y1 * y1 - z1 * z1;
    double t2 = 0.5 - x2 * x2 - y2 * y2 - z2 * z2;
    double t3 = 0.5 - x3 * x3 - y3 * y3 - z3 * z3;


    if (t0 < 0) {
      n0 = 0.0;
    } else {
      int gi0 = this.perm[ii + this.perm[jj + this.perm[kk]]] & 15;
      t0 *= t0;
      n0 = t0 * t0 * (this.grad[gi0][0] * x0 + this.grad[gi0][1] * y0 + this.grad[gi0][2] * z0);
    }

    if (t1 < 0) {
      n1 = 0.0;
    } else {
      int gi1 = this.perm[ii + i1 + this.perm[jj + j1 + this.perm[kk + k1]]] & 15;
      t1 *= t1;
      n1 = t1 * t1 * (this.grad[gi1][0] * x1 + this.grad[gi1][1] * y1 + this.grad[gi1][2] * z1);
    }

    if (t2 < 0) {
      n2 = 0.0;
    } else {
      int gi2 = this.perm[ii + i2 + this.perm[jj + j2 + this.perm[kk + k2]]] & 15;
      t2 *= t2;
      n2 = t2 * t2 * (this.grad[gi2][0] * x2 + this.grad[gi2][1] * y2 + this.grad[gi2][2] * z2);
    }

    if (t3 < 0) {
      n3 = 0.0;
    } else {
      int gi3 = this.perm[ii + 1 + this.perm[jj + 1 + this.perm[kk + 1]]] & 15;
      t3 *= t3;
      n3 = t3 * t3 * (this.grad[gi3][0] * x3 + this.grad[gi3][1] * y3 + this.grad[gi3][2] * z3);
    }

    // Add contributions from each corner to get the final noise value.
    // The result is scaled to return values in the interval [-1,1].
    return 32.0 * (n0 + n1 + n2 + n3);
  }
}