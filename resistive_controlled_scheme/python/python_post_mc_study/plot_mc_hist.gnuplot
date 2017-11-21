#!/usr/bin/gnuplot

set grid
set style line 11 lc rgb '#333333' lt 1
set border 3 back ls 11
set tics nomirror


# color definitions
set style line 1  lc rgb '#8e0200' lt 1 lw 1 pt 6 ps 1 # ---red
set style line 2  lc rgb '#007ea7' lt 1 lw 2 pt 7 # -- remaining blues and greens
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


set xlabel "Read Resistance [KOhms]"
set ylabel "Ocurrences"
set title 'Histogram under RRAM/CMOS variability'

# call histogram function
# binwidth = 4
# binstart = -98
# load 'hist.fct'


input_file = 'exported_results_montecarlo/full_range_r_read/1r_g_1_raw.data'
input_file = 'exported_results_montecarlo/clip_range_r_read/1t1r_g_1_raw.data'

set style fill solid 0.5 # fill style

set output "hist.svg"

#plot for[i=1:31] input_file u (hist(column(i+0),width)):(1.0) smooth freq w boxes ls 1 notitle

# store max/min vals for bins computation
############################
## Requires gnuplot 5.2!!
###########################
array maxes[31]
array mines[31]
array widths[31]
n=10 # number of intervals
set term svg noenhanced #size 1800,1000 fname 'Times' #fsize 35
do for [i=1:31]{
	
	set output '/dev/null'
	set autoscale xmin
	set autoscale xmax
	plot input_file using i:i
	maxes[i]=GPVAL_DATA_X_MAX
	mines[i]=GPVAL_DATA_X_MIN
	widths[i] = (maxes[i]-mines[i])/n
	# print min
	# print widths[i]
}

set term svg noenhanced size 1800,1000 font 'Times,35' # fname 'Times' #fsize 35
set output "hist.svg"

#function used to map a value to the intervals
hist(x,width)=width*floor(x/width)+width/2.0
color(x) = x>180?360-x:x
set boxwidth widths[15]*0.9
plot for[i=1:31] input_file u (hist(column(i+0),widths[i])):(1.0) smooth freq w boxes ls i notitle

unset output
quit
