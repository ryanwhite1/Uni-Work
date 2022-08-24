set style line 1 \
    linecolor rgb '#0060ad' \
    linetype 1 linewidth 1 \
    pointtype 7 pointsize 0.5

set style line 2 \
    linecolor rgb '#fc2803' \
    linetype 1 linewidth 1 \
    pointtype 7 pointsize 0.5


set terminal pdf
set output "Q2a.pdf"
set xlabel "x"
set ylabel "y"
set title "Exponential Model Data"
plot "exp-model-distribution.dat" with linespoints ls 1 title "Data"



set term pdf size 9, 4.5
set output "Q2b1.pdf"
set xlabel "x"
set ylabel "y"
set title "Interpolated Data vs Highly Sampled Data"
set tics font ", 16"
set multiplot layout 2, 1
set yrange[-0.05:0.5]
plot "Q2Interp.dat" with linespoints ls 1 title "Interpolated Data", \
    "Q2HighSampled.dat" with linespoints ls 2 title "Highly Sampled Function"
set yrange[-0.0006:0.0016]
plot "Q2Residuals.dat" with linespoints ls 1 title "Residuals"