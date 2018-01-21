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

####################
## second file
####################
output_file='exported_gnuplot/'
input_file_1 = 'exported_results_nominal/clip_range_r_read/1t1r_calibrated_load_resistances.data'
input_file_2 = 'exported_results_nominal/clip_range_r_read/1t1r_read_r_for_calibrated_load_resistances.data'
# g between 0-5
selected_g = 2+1

set term svg noenhanced size 1000,1500 fname 'Times' font 'Times,40' # fname 'Times' #fsize 35

set output output_file."final_selected_loads.svg"


set multiplot layout 2,1
# set lmargin 10
# set bmargin 2
unset lmargin
unset bmargin

set xrange[0:30]

unset key

set xlabel "Level"
set ylabel "Load Resistance [KOhms]"
set title '1T1R cell Used R_LOAD'
plot input_file_1 u  (1e-3*($3)) w lp ls 3 ps 0.5  axes x1y1


set xlabel "Level"
set ylabel "Read Resistance at 0.1V [KOhms]"
set title '1T1R cell Achieved Read Resistance'
plot input_file_2 u  (1e-3*($3)) w lp ls 3 ps 0.5  axes x1y1

set key title 'Initial CF length'

unset multiplot
unset output

quit
