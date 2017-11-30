
set grid
# set border 4095
set format x "%g"
set format y "%g"
set format z "%g"
set format cb "%g"

# color definitions
set style line 1  lc rgb '#cf3a00' lt 1 lw 1 pt 6 ps 1 # ---red
set style line 2  lc rgb '#0025ad' lt 1 lw 2 pt 7 # -- remaining blues and greens
set style line 3  lc rgb '#0042ad' lt 1 lw 2
set style line 4  lc rgb '#0060ad' lt 1 lw 2
set style line 5  lc rgb '#007cad' lt 1 lw 2
set style line 6  lc rgb '#0099ad' lt 1 lw 2
set style line 7 lc rgb '#00ada4' lt 1 lw 2
set style line 8 lc rgb '#00ad88' lt 1 lw 2
set style line 9 lc rgb '#00ad6b' lt 1 lw 2
set style line 10 lc rgb '#00ad4e' lt 1 lw 2
set style line 11 lc rgb '#00ad31' lt 1 lw 2
set style line 12 lc rgb '#00ad14' lt 1 lw 2
set style line 13 lc rgb '#09ad00' lt 1 lw 2
set style fill solid
# interpolates 3d plots
# set pm3d interpolate 5,5
# shows lines between surfaces triangles
set pm3d depthorder
# removes hidden lines
set pm3d hidden3d
# removes hidden lines
# set hidden3d
# sets 3d object properties
set style fill transparent solid 0.8 border
#set style fill transparent solid 0.8 noborder
# set pm3d at st
# set pm3d scansautomatic flush begin noftriangles nohidden3d solid implicit corners2color mean

# sets plane to ground
set ticslevel 0
# sets box arround 3d plot
set border 4095
# sets grid
set grid

#set view 60,15

# set cbrange [0:100]
# set zrange [0:100.00001]
set view 120,60
# set view 60,110

# set palette defined ( 0 "#C1DAE8", 1e-19 "#fffaef", 50 "#ffd35a", 100 "#ed2c29")
set palette defined ( 0 "#ed2c29", 10 "#ffd35a", 50 "#fffaef", 100 "#C1DAE8")

set term svg noenhanced size 1200,900 fname 'Times' fsize 25

# set logscale z
set format z "%2.0te%L"
set format cb "%2.0te%L" 
set title "dCF/dt"
set xlabel "Cell Voltage [V]"
set ylabel "CF's length [nm]"
set zlabel "dCF / dt.  CF evolution speed[m/s]" rotate by 90

set output "cf_ddt.svg"
splot 'exported_data/gap_ddt.data' u ($1):(5 - 1e9*($2)):(abs($3)) notitle linecolor rgb '#333333' linewidth 0.3 w pm3d
# splot 'exported_data/gap_ddt2.data' u ($1):(1e9*($2)):3 notitle  w pm3d
unset output

quit
