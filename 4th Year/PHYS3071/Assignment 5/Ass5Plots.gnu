set terminal pdf
set output "PartA.pdf"
set xlabel "time (arbitrary time units)"
set ylabel "x (arbitrary space units)"
set cblabel "Probability (|Ψ|^2)"
set title ""

set xrange[0:1.56923]
set yrange[-4:4]
plot "PartA.dat" using 1:2:3 with image notitle

set output "PartB.pdf"
plot "PartB.dat" using 1:2:3 with image notitle

set output "PartC.pdf"
plot "PartC.dat" using 1:2:3 with image notitle