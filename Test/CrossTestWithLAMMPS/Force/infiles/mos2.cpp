#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h> 

const int Nx = 50;
const int Ny = 30;
const int N  = Nx * Ny;
int main(int argc, char *argv[])
{
    double a = 3.16/sqrt(3.0);
    double Lx = Nx * sqrt(3.0) * 0.5 * a;
    double Ly = Ny * 1.5 * a;
    double Lz = 6.09;
    FILE *fid = fopen("xyz.in", "w");
    fprintf(fid, "%10d%10d%10.1f\n", N*3/2, 15, 3.8); 
    fprintf(fid, "%10d%10d%10d%25.15f%25.15f%25.15f\n", 1, 1, 0, Lx, Ly, Lz);
    FILE *fid1 = fopen("in.xyz", "w");
    fprintf(fid1, "%10d%10d%10.1f\n", N*3/2, 15, 3.8);
    fprintf(fid1, "%10d%10d%10d%25.15f%25.15f%25.15f\n", 1, 1, 0, Lx, Ly, Lz);
    for (int nx = 0; nx < Nx; ++nx)
    {
        for (int ny = 0; ny < Ny; ++ny)
        {
            double x = nx * sqrt(3.0) * 0.5 * a;
            double y = ny * 1.5 * a;  
            if (nx%2 == ny%2) // Mo
            {
                y += 0.5 * a;
                fprintf(fid, "%10d%10d%10.1f%25.15f%25.15f%25.15f\n", 0, 0, 96.0, x, y, 0.0);
                fprintf(fid1, "%10d%25.15f%25.15f%25.15f\n", 42, x, y, 0.0);
            }
            else // S
            {
                fprintf(fid, "%10d%10d%10.1f%25.15f%25.15f%25.15f\n", 1, 0, 32.0, x, y, +1.591);
                fprintf(fid, "%10d%10d%10.1f%25.15f%25.15f%25.15f\n", 2, 0, 32.0, x, y, -1.591);
                fprintf(fid1, "%10d%25.15f%25.15f%25.15f\n", 16, x, y, +1.591);
                fprintf(fid1, "%10d%25.15f%25.15f%25.15f\n", 16, x, y, -1.591);
            }
        }
    }
    fclose(fid);
    return 0;
}