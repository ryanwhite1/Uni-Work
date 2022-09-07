set terminal pdf
set output "Q2b-Heatmap.pdf"
set xlabel "x"
set ylabel "y"
set title ""

set xrange[0:1001]
set yrange[0:1001]
plot "2b-XYZ.dat" using 1:2:3 with image notitle