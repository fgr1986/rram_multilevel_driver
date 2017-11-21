#!/usr/bin/gnuplot

set grid
set style line 11 lc rgb '#333333' lt 1
set border 3 back ls 11
set tics nomirror


# color definitions
# set style line 1  lc rgb '#8e0200' lt 1 lw 1 pt 6 ps 1 # ---red
# set style line 2  lc rgb '#007ea7' lt 1 lw 2 pt 7 # -- remaining blues and greens
# set style line 3  lc rgb '#0042ad' lt 1 lw 2 pt 8
# set style line 1 lt 1 lw 4 pt 6 ps 0.3 lc rgb '#0072bd' # blue ps variable
# set style line 2 lt 1 lw 4 pt 7 ps 0.5 lc rgb '#ff0000' # other colors
# set style line 3 lt 1 lw 4 pt 7 ps 0.5 lc rgb '#ff7800' # other colors
# set style line 4 lt 1 lw 4 pt 7 ps 0.5 lc rgb '#4ec000' # other colors
# set style line 5 lt 1 lw 4 pt 7 ps 0.5 lc rgb '#a049c0' # other colors
# set style line 6 lt 1 lw 4 pt 7 ps 0.5 lc rgb '#8e0200' # other colors

load 'moreland.pal'
set style line 1 lt 1 lw 4 pt 6 ps 0.5 lc palette
set style fill solid

unset colorbox

set format x "%g"
set format y "%g"
# set lmargin 10
# set bmargin 2


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

set term svg noenhanced size 1800,1000 fname 'Times' fsize 35
set output "cdf.svg"

set xlabel "Read Resistance [KOhms]"
set ylabel "CDF"
set title 'CDF under RRAM/CMOS variability'
input_file = 'exported_results_montecarlo/full_range_r_read/1r_g_2_cdf.data'


color(x) = x>180?360-x:x
plot for [i=1:64:2] input_file u (1e-3*column(i)):(column(i+1)):color(i) w lp ls 1 axes x1y1 notitle
 

unset output


quit
