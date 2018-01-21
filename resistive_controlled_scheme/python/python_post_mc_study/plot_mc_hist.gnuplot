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

set style fill solid 0.5 # fill style

# only intra device variability
# base_folder = 'exported_results_montecarlo/only_intra_device_variability/full_range/'
# output_folder = 'exported_gnuplot/only_intra_device_variability/full_range/'
# m_title = '1t1r_full_range_hist_g'

# inter intra device variability
# both clip_range and full_range
base_folder = 'exported_results_montecarlo/inter_intra_device_variability/clip_range/'
output_folder = 'exported_gnuplot/inter_intra_device_variability/clip_range/'
m_title = '1t1r_clip_range_hist_g'
# base_folder = 'exported_results_montecarlo/inter_intra_device_variability/full_range/'
# output_folder = 'exported_gnuplot/inter_intra_device_variability/full_range/'
# m_title = '1t1r_full_range_hist_g'

cell_type = '1t1r'
mc_num = 1000
# for full
# dist_r(g_idx) = g_idx==0 ? 100 : g_idx<3 ? 200 : g_idx==3 ? 400 : g_idx==4 ? 500 : 600
# for clip
dist_r(g_idx) = g_idx<3 ? 100 : 200
max_r(g_idx) = g_idx==0 ? 700 : g_idx<3 ? 1300 : g_idx==3 ? 1900 : g_idx==4 ? 3000 : 3700

# full_range 
levels_dist(g_idx) = 1
# clip_range
# levels_dist(g_idx) = g_idx < 3 ? 1 : 2

# store max/min vals for bins computation
############################
## Requires gnuplot 5.2!!
###########################
# for 6 different initial HRS
# cfs = [1.2, 1.3, 1.367, 1.5, 1.6, 1.7]
init_cf(g_idx) = g_idx==2 ? 5-1.367 : 5-(1.2 + 0.1*g_idx)

full_size = 32*6
array maxes[32*6]
array mines[32*6]
array widths[32*6]
n=10 # number of intervals
set term svg noenhanced #size 1800,1000 fname 'Times' #fsize 35

print 'Preprocessing files'
set output '/dev/null'
do for[g=0:5]{
	input_file = base_folder.'/'.cell_type.'_g_'.g.'_raw.data'
	print 'file: '.input_file
	do for [i=1:32:levels_dist(g)]{
		# set autoscale xmin
		# set autoscale xmax
		plot input_file using i:i
		maxes[32*g+i]=GPVAL_DATA_X_MAX
		mines[32*g+i]=GPVAL_DATA_X_MIN
		widths[32*g+i] = 1e-3*(maxes[32*g+i]-mines[32*g+i])/n
		print '    processing g_'.g.' l_'.i
	}
}

#function used to map a value to the intervals
hist(x,width)=(width*floor(1e-3*x/width)+width/2.0)
color(x) = x>180?360-x:x

set term svg noenhanced size 1200,600 font 'Times,25' # fname 'Times' #fsize 35
do for[g=0:5]{
	set output output_folder.m_title.g.'.svg'
	cf = init_cf(g)
	scf = sprintf("%g", cf)
	set title 'Initial CF length '.scf.' nm'
	input_file = base_folder.'1t1r_g_'.g.'_raw.data'
	
	set yrange [0:]
	plot for[i=1:32:levels_dist(g)] input_file u (hist(column(i+0),widths[32*g+i])):(1.0) smooth freq w boxes ls i notitle
	unset output
}


set output output_folder.'final_'.m_title.'.svg'
unset title
# set boxwidth widths[15]*0.9

# set term svg noenhanced size 600,2200 font 'Times,25' # fname 'Times' #fsize 35
# set multiplot layout 6,1

# set term svg noenhanced size 3200,1200 font 'Times,35' # fname 'Times' #fsize 35
# set multiplot layout 2,3

set term svg noenhanced size 2000,3000 font 'Times,48' # fname 'Times' #fsize 35
set multiplot layout 3,2



do for[g=0:5]{
	input_file = base_folder.'1t1r_g_'.g.'_raw.data'
	print input_file
	cf = init_cf(g)
	scf = sprintf("%g", cf)
	set title 'Initial CF length '.scf.' nm'
	set xtics 0,dist_r(g),max_r(g)
	
	set yrange [0:]
	plot for[i=1:32:levels_dist(g)] input_file u (hist(column(i+0),widths[32*g+i])):(1.0) smooth freq w boxes ls i notitle
}
unset multiplot
# set xrange [mines[1]:maxes[32]]
unset output

# set term svg noenhanced size 1800,1000 font 'Times,35' # fname 'Times' #fsize 35
# unset xrange
# set output "hist_detail.svg"
# set multiplot layout 2,2

# set boxwidth 0.1
# do for[i=10:25:5]{
# 	set boxwidth widths[i]*0.9
# 	plot input_file u (hist(column(i+0),widths[(i+0)])):(1.0) smooth freq w boxes ls i notitle
# }

# unset multiplot
# unset output
quit
