set terminal pdf

set title ""

set style line 1 \
    linecolor rgb '#0060ad' \
    linetype 1 linewidth 2 \
    pointtype -1 pointsize 1.5

set style line 2 \
    linecolor rgb '#b51f1f' \
    linetype 1 linewidth 2 \
    pointtype -1 pointsize 1.5

set style line 3 \
    linecolor rgb '#368df7' \
    linetype 1 linewidth 2 \
    pointtype -1 pointsize 1.5

set style line 4 \
    linecolor rgb '#fa7f14' \
    linetype 1 linewidth 2 \
    pointtype -1 pointsize 1.5

set style line 5 lc rgb 'blue' pt 7 pointsize 1
set style line 6 lc rgb 'red' pt 7 pointsize 1
set style line 7 lc rgb 'black' pt 7 pointsize 1

set grid

set yrange[-0.5:1.5]
set xrange[-1:1]
set size ratio -1
set xlabel "x (units)"
set ylabel "y (units)"
set output "CometOrbit.pdf"
plot "Q1c.dat" using 1:2 with lines linestyle 1 title "Orbital Path", \
    "<echo '0 1'" with points ls 5 title "r(t1)", \
    "<echo '0.4416 0.2345'" with points ls 6 title "r(t2)", \
    "<echo '0 0'" with points ls 7 title "Focus"