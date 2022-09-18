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

set grid


set xlabel "Time (s)"
set ylabel "Energy (J)"
set output "EulerMethod1Energy.pdf"
plot "EulerMethod1.dat" using 5:6 with lines linestyle 1 title "Energy"

set output "EulerMethod2Energy.pdf"
plot "EulerMethod2.dat" using 5:6 with lines linestyle 1 title "Energy"

set output "BothCoolEnergy.pdf"
plot "EulerCool.dat" using 5:6 with lines linestyle 1 title "Euler Energy", \
    "RK4Cool.dat" using 5:6 with lines linestyle 2 title "RK4 Energy"

set output "RK4Method1Energy.pdf"
plot "RK4Method1.dat" using 5:6 with lines linestyle 1 title "Energy"

set output "RK4Method2Energy.pdf"
plot "RK4Method2.dat" using 5:6 with lines linestyle 1 title "Energy"

set yrange[-2:3]
set xrange[-2:2]
set size ratio -1

set xlabel "x (m)"
set ylabel "y (m)"
set output "EulerMethod1.pdf"
plot "EulerMethod1.dat" using 1:2 with lines linestyle 1 title "Inner Pendulum", \
    "EulerMethod1.dat" using 3:4 with lines linestyle 2 title "Outer Pendulum"

set output "EulerMethod2.pdf"
plot "EulerMethod2.dat" using 1:2 with lines linestyle 1 title "Inner Pendulum", \
    "EulerMethod2.dat" using 3:4 with lines linestyle 2 title "Outer Pendulum"

set output "RK4Method1.pdf"
plot "RK4Method1.dat" using 1:2 with lines linestyle 1 title "Inner Pendulum", \
    "RK4Method1.dat" using 3:4 with lines linestyle 2 title "Outer Pendulum"

set output "RK4Method2.pdf"
plot "RK4Method2.dat" using 1:2 with lines linestyle 1 title "Inner Pendulum", \
    "RK4Method2.dat" using 3:4 with lines linestyle 2 title "Outer Pendulum"

set output "BothMethodsCool.pdf"
plot "EulerCool.dat" using 1:2 with lines linestyle 1 title "Inner Euler Pendulum", \
    "EulerCool.dat" using 3:4 with lines linestyle 2 title "Outer Euler Pendulum", \
    "RK4Cool.dat" using 1:2 with lines linestyle 3 title "Inner RK4 Pendulum", \
    "RK4Cool.dat" using 3:4 with lines linestyle 4 title "Outer RK4 Pendulum"
