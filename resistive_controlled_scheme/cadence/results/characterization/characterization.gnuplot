set grid
set style line 11 lc rgb '#333333' lt 1
set border 3 back ls 11
set tics nomirror


# color definitions
# set style line 1  lc rgb '#8e0200' lt 1 lw 1 pt 6 ps 1 # ---red
# set style line 2  lc rgb '#007ea7' lt 1 lw 2 pt 7 # -- remaining blues and greens
# set style line 3  lc rgb '#0042ad' lt 1 lw 2 pt 8
set style line 1 lt 1 lw 4 pt 7 ps 0.5 lc rgb '#0072bd' # blue ps variable
set style line 2 lt 1 lw 4 pt 7 ps 0.5 lc rgb '#ff0000' # other colors
set style line 3 lt 1 lw 4 pt 7 ps 0.5 lc rgb '#ff7800' # other colors
set style line 4 lt 1 lw 4 pt 7 ps 0.5 lc rgb '#4ec000' # other colors
set style line 5 lt 1 lw 4 pt 7 ps 0.5 lc rgb '#a049c0' # other colors
set style fill solid

set term svg noenhanced size 1200,1400 fname 'Times' fsize 30
set output "characterization.svg"
set xlabel "time [ns]"
set ylabel "Voltage [V]"
set title "Abrupt SET & gradual RESET  HfO2 Example"
# set y2tics
set key top left # right

set format x "%g"
set format y "%g"
set multiplot layout 3, 1
set lmargin 10
set bmargin 2

set xrange [0:50]


set datafile separator ","

# number of tics

plot 'set_characterization.data' u (1e9*($1)):($2) every 30 w lp ls 1 ps 0.5  axes x1y1 title 'SET', \
	'reset_characterization.data' u (1e9*($1)):($2) every 30 w lp ls 2 ps 0.5  axes x1y1 title 'RESET'

set ylabel "CF's Length [nm]"
# set key top right
# set xrange [10:18]

set ytics 0,0.3,5
# set yrange[0:5]
plot 'set_characterization.data' u (1e9*($1)):(5-1e9*($4)) every 30 w lp ls 1 ps 0.5  axes x1y1 title 'SET', \
	'reset_characterization.data' u (1e9*($1)):(5-1e9*($4)) every 30 w lp ls 2 ps 0.5  axes x1y1 title 'RESET'


unset yrange
set ylabel "Current [mA]"
# number of tics

set logscale y
set ytics 1e-4, 1e-2,1
# set ytics 0.01, 1, 100, 10000
plot 'set_characterization.data' u (1e9*($1)):(1e3*($6)) every 30 w lp ls 1 ps 0.5  axes x1y1 title 'SET', \
	'reset_characterization.data' u (1e9*($1)):(1e3*abs($6)) every 30 w lp ls 2 ps 0.5  axes x1y1 title 'RESET'


unset multiplot
unset output

quit
