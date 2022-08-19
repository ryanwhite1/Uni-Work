set terminal pdf
set output "Q1c1.pdf"
set xlabel "x"
set ylabel "y"
set title "Iteration 1"

set style line 1 \
    linecolor rgb '#0060ad' \
    linetype 1 linewidth 2 \
    pointtype 7 pointsize 1.5

plot "Q1data1.dat" using 2:3 with linespoints

set output "Q1c2.pdf"
set xlabel "x"
set ylabel "y"
set title "Iteration 2"

set style line 1 \
    linecolor rgb '#0060ad' \
    linetype 1 linewidth 2 \
    pointtype 7 pointsize 1.5

plot "Q1data2.dat" using 2:3 with linespoints

set output "Q1c3.pdf"
set xlabel "x"
set ylabel "y"
set title "Iteration 3"

set style line 1 \
    linecolor rgb '#0060ad' \
    linetype 1 linewidth 2 \
    pointtype 7 pointsize 1.5

plot "Q1data3.dat" using 2:3 with linespoints