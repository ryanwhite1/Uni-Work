set terminal pdf
set output "Q2a-Heatmap.pdf"
set xlabel "x"
set ylabel "y"
set title ""

plot "2a-XYZ.dat" using 1:2:3 with image notitle