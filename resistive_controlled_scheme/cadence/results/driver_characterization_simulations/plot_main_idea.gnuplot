# plots the transient of different r_read

set term svg enhanced size 1500,800 fname 'Times' fsize 35
set output "different_responses.svg"
set grid
set format x "%g"
set format y "%g"
set xlabel "Time [ns]" offset 0,0.5
set ylabel "Cell Read Resistance at 0.1V [Kohm]" offset 1,0
set style line 11 lc rgb '#333333' lt 1
set border 3 back ls 11
set tics nomirror

set palette defined ( 0 "#C1DAE8", 1e-19 "#fffaef", 50 "#ffd35a", 100 "#ed2c29")

# color definitions
set style line 1 lt 1 lw 4 pt 7 ps 0.5 lc rgb '#0072bd' # blue ps variable
set style line 2 lt 1 lw 4 pt 7 ps 0.5 lc rgb '#ff0000' # other colors
set style line 3 lt 1 lw 4 pt 7 ps 0.5 lc rgb '#ff7800' # other colors
set style line 4 lt 1 lw 4 pt 7 ps 0.5 lc rgb '#4ec000' # other colors
set style line 5 lt 1 lw 4 pt 7 ps 0.5 lc rgb '#a049c0' # other colors


# set style fill transparent solid 1

set key center right

set title "Read Resistance at 0.1V"

set datafile separator ","
# 6 cells (g_0-g_5), each with different gaps
# data is, by colums: X, g_0_r_read_level_0, X, g_0_r_read_level_1...., g_1_r_read_level_0...
# 1024 levels for each cell

set multiplot layout 1, 2

set title "Lower Initial HRS"
plot 'nominal_g_0-5_1r_all.csv' u (1e9*($1)):(($200)/1e3)  every 30  w lp ls 1 notitle, \
    'nominal_g_0-5_1r_all.csv' u (1e9*($1)):(($800)/1e3)  every 30  w lp ls 2 notitle, \
    'nominal_g_0-5_1r_all.csv' u (1e9*($1)):(($1000)/1e3)  every 30  w lp ls 3 notitle, \

set title "Higher Initial HRS"
plot 'nominal_g_0-5_1r_all.csv' u (1e9*($1)):(($10440)/1e3)  every 30  w lp ls 1 notitle, \
    'nominal_g_0-5_1r_all.csv' u (1e9*($1)):(($11040)/1e3)  every 30  w lp ls 2 notitle, \
    'nominal_g_0-5_1r_all.csv' u (1e9*($1)):(($11240)/1e3)  every 30  w lp ls 3 notitle, \

unset multiplot
unset output

quit
