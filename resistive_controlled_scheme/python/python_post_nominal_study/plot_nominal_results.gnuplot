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

set term svg noenhanced size 1400,1400 fname 'Times' fsize 35
# set y2tics
set key top left # right

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
# r_loads: 250, 500, 750... 256k
################
# file 1, read Resistances

set output "read_resistances.svg"
set xlabel "Load resistance [kOhms]"
set ylabel "Read resistance  at 0.1V [kOhms]"

set multiplot layout 2,1

set title '1R cell'
plot 'exported_results_nominal/full_range_r_read/1r_simulated_read_resistance.data' u (1e-3*($1)):(1e-3*($2)) every 10 w lp ls 1 ps 0.5  axes x1y1 title '1.2nm', \
		'exported_results_nominal/full_range_r_read/1r_simulated_read_resistance.data' u (1e-3*($1)):(1e-3*($3)) every 10 w lp ls 2 ps 0.5  axes x1y1 title '1.3nm', \
		'exported_results_nominal/full_range_r_read/1r_simulated_read_resistance.data' u (1e-3*($1)):(1e-3*($4)) every 10 w lp ls 3 ps 0.5  axes x1y1 title '1.367nm', \
		'exported_results_nominal/full_range_r_read/1r_simulated_read_resistance.data' u (1e-3*($1)):(1e-3*($5)) every 10 w lp ls 4 ps 0.5  axes x1y1 title '1.5nm', \
		'exported_results_nominal/full_range_r_read/1r_simulated_read_resistance.data' u (1e-3*($1)):(1e-3*($6)) every 10 w lp ls 5 ps 0.5  axes x1y1 title '1.6nm', \
		'exported_results_nominal/full_range_r_read/1r_simulated_read_resistance.data' u (1e-3*($1)):(1e-3*($7)) every 10 w lp ls 6 ps 0.5  axes x1y1 title '1.7nm', \

set title '1T1R cell'
plot 'exported_results_nominal/full_range_r_read/1t1r_simulated_read_resistance.data' u (1e-3*($1)):(1e-3*($2)) every 10 w lp ls 1 ps 0.5  axes x1y1 , \
	'exported_results_nominal/full_range_r_read/1t1r_simulated_read_resistance.data' u (1e-3*($1)):(1e-3*($3)) every 10 w lp ls 2 ps 0.5  axes x1y1 , \
	'exported_results_nominal/full_range_r_read/1t1r_simulated_read_resistance.data' u (1e-3*($1)):(1e-3*($4)) every 10 w lp ls 3 ps 0.5  axes x1y1 , \
	'exported_results_nominal/full_range_r_read/1t1r_simulated_read_resistance.data' u (1e-3*($1)):(1e-3*($5)) every 10 w lp ls 4 ps 0.5  axes x1y1 , \
	'exported_results_nominal/full_range_r_read/1t1r_simulated_read_resistance.data' u (1e-3*($1)):(1e-3*($6)) every 10 w lp ls 5 ps 0.5  axes x1y1 , \
	'exported_results_nominal/full_range_r_read/1t1r_simulated_read_resistance.data' u (1e-3*($1)):(1e-3*($7)) every 10 w lp ls 6 ps 0.5  axes x1y1 , \

unset multiplot
unset output

quit
