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
set style line 6 lt 1 lw 4 pt 7 ps 0.5 lc rgb '#8e0200' # other colors
set style fill solid

set format x "%g"
set format y "%g"
set lmargin 10
set bmargin 2

# set xrange [0:50]


set datafile separator ","

################
## simulation Parameters
# gaps
# [1.2e-9, 1.3e-9, 1.367e-9, 1.5e-9, 1.6e-9, 1.7e-9]
# lengths: 5-gap
# []
# r_loads: 250, 500, 750... 256k


################
# file 1, read Resistances
#############################

set term svg noenhanced size 1400,1800 fname 'Times' fsize 35
set output "read_resistances.svg"
set xlabel "Load resistance [kOhms]"
set ylabel "Read resistance  at 0.1V [kOhms]"

set multiplot layout 3,1

unset key
set title '1R cell'
plot 'exported_results_nominal/full_range_r_read/1r_simulated_read_resistance.data' u (1e-3*($1)):(1e-3*($2)) every 10 w lp ls 1 ps 0.5  axes x1y1 , \
		'exported_results_nominal/full_range_r_read/1r_simulated_read_resistance.data' u (1e-3*($1)):(1e-3*($3)) every 10 w lp ls 2 ps 0.5  axes x1y1 , \
		'exported_results_nominal/full_range_r_read/1r_simulated_read_resistance.data' u (1e-3*($1)):(1e-3*($4)) every 10 w lp ls 3 ps 0.5  axes x1y1 , \
		'exported_results_nominal/full_range_r_read/1r_simulated_read_resistance.data' u (1e-3*($1)):(1e-3*($5)) every 10 w lp ls 4 ps 0.5  axes x1y1 , \
		'exported_results_nominal/full_range_r_read/1r_simulated_read_resistance.data' u (1e-3*($1)):(1e-3*($6)) every 10 w lp ls 5 ps 0.5  axes x1y1 , \
		'exported_results_nominal/full_range_r_read/1r_simulated_read_resistance.data' u (1e-3*($1)):(1e-3*($7)) every 10 w lp ls 6 ps 0.5  axes x1y1 , \

set title '1T1R cell'
plot 'exported_results_nominal/full_range_r_read/1t1r_simulated_read_resistance.data' u (1e-3*($1)):(1e-3*($2)) every 10 w lp ls 1 ps 0.5  axes x1y1 , \
	'exported_results_nominal/full_range_r_read/1t1r_simulated_read_resistance.data' u (1e-3*($1)):(1e-3*($3)) every 10 w lp ls 2 ps 0.5  axes x1y1 , \
	'exported_results_nominal/full_range_r_read/1t1r_simulated_read_resistance.data' u (1e-3*($1)):(1e-3*($4)) every 10 w lp ls 3 ps 0.5  axes x1y1 , \
	'exported_results_nominal/full_range_r_read/1t1r_simulated_read_resistance.data' u (1e-3*($1)):(1e-3*($5)) every 10 w lp ls 4 ps 0.5  axes x1y1 , \
	'exported_results_nominal/full_range_r_read/1t1r_simulated_read_resistance.data' u (1e-3*($1)):(1e-3*($6)) every 10 w lp ls 5 ps 0.5  axes x1y1 , \
	'exported_results_nominal/full_range_r_read/1t1r_simulated_read_resistance.data' u (1e-3*($1)):(1e-3*($7)) every 10 w lp ls 6 ps 0.5  axes x1y1 , \

set key title 'Initial CF length'
# set key below
set key center center
set border 0
unset tics
unset xlabel
unset ylabel
set yrange [0:1]
plot 2 w lp ls 1 t '3.8 nm', \
     2 w lp ls 2 t '3.7 nm', \
     2 w lp ls 3 t '3.636 nm', \
		 2 w lp ls 4 t '3.5 nm', \
		 2 w lp ls 5 t '3.4 nm', \
		 2 w lp ls 6 t '3.3 nm'

unset border
unset yrange
set tics
set xlabel
set ylabel

unset multiplot
unset output
