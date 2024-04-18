#include <iostream>
#include <fstream> // ofstream: write to files, ifstream: read from files, fstream: both read and write
#include <vector>
#include <cmath>
#include <time.h>
#include <chrono>  // for high_resolution_clock

int main() {

  // Set up variables here

  // Set up a vector for the multiplicity (of each magnetisation macrostate). Initiate it with zeros:
  // mult = [0, 0, 0, 0, ...] Make sure to get the length correct!

  for (int s1=-1; s1 <= 1; s1+=2) {   // in steps of 2 for spin-half system (-1 spin-down, +1 spin-up)
    for (int s2=-1; s2 <= 1; s2+=2) {
      for (int s3=-1; s3 <= 1; s3+=2) {
        for (int s4=-1; s4 <= 1; s4+=2) {
          for (int s5=-1; s5 <= 1; s5+=2) {
        // Add more loops for more spins here

              // Inside all loops, calculate desired quantities:
              // spinTotal = s1 + s2 + ...

              // 1. Energy of state, E_m = mu*B*spinTotal
              // 2. Statistical weight of state [i.e. Boltzmann factor, exp(-E_m/(kB*T))]
              // 3. Magnetisation of state, mag_m = spinTotal/N

              // 4. Running sum of weights           (for partition function)
              // 5. Running sum of E_m*weight        (for <E>)
              // 6. Running sum of magnetisation*weight (for <M>)

              // 7. Running sum of multiplicity for this magnetisation: mult[spinTotal+N]+=1 (the +N here ensures that the minimum vector index is 0)
          }
        }
      }
    }
  }

  // At the end, normalise your <E> and <M> measurements by Z.

  // Save the multiplicity vector to a file so that you can plot it.

  return 0;
}