# import plotly.plotly as py
import plotly.offline
from plotly.graph_objs import Scatter, Layout
import numpy as np
import pandas as pd
import sys
import os


############################
# Useful functions
############################
def find_nearest(array, value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]


def find_nearest_sorted(sorted_array, value):
    idx = np.searchsorted(sorted_array, value, side="left")
    if (idx > 0 and (
        idx == len(sorted_array)
        or abs(value - sorted_array[idx-1]) < abs(value-sorted_array[idx]))):
        return sorted_array[idx-1], idx-1
    else:
        return sorted_array[idx], idx


############################
# Parameters
############################
# To obtain the target resistances/resistive loads
# initial gaps defined in the netlists
initial_gaps = np.array([1.2e-9, 1.3e-9, 1.367e-9, 1.5e-9, 1.6e-9, 1.7e-9])
# maximum r_load, to avoid varaibility, per gap
clip_r_read = True
maximum_r_read = np.array([0.5e6, 0.6e6, 0.7e6, 0.8e6, 0.8e6, 0.8e6])
# data from ../stand_alone_simulations/resistive_controlled_scheme/results
print('\n\tPrinting data for every gap in ' + str(initial_gaps) + '\n\n')
cell = '1t1r'
print('\tCell type: ' + cell)
data_file = '../../cadence/results/nominal_results/nominal_g_0-5_' + cell + '_last.csv'
n_gaps = initial_gaps.shape[0]
simulated_levels = 1024
target_levels = 32
r_load_min = 0.25e3
print('\tSimulated levels (' + str(r_load_min) + '  ohms per level): '
      + str(simulated_levels))
print('\tComputed levels: ' + str(target_levels))
r_loads = np.linspace(r_load_min,
                      simulated_levels*r_load_min, simulated_levels)
if clip_r_read:
    generated_files_folder = 'exported_results_nominal/clip_range_r_read/'
    pre = generated_files_folder + cell + '_'
else:
    generated_files_folder = 'exported_results_nominal/full_range_r_read/'
    pre = generated_files_folder + cell + '_'
############################
# preparing folder
############################
# create final folder
if not os.path.exists(generated_files_folder):
    os.makedirs(generated_files_folder)

############################
# Plotly configuration
############################
plotly.tools.set_config_file(world_readable=False,
                             sharing='private')

############################
# Import data
############################
full_data = np.genfromtxt(data_file, delimiter=',')

############################
# r_read vs r_load
############################

# data in X0 Y0, X1, Y1 format, grab all Y values
last_r_read = np.array([full_data[full_data.shape[0]-1, 1::2]])
r_length = int(last_r_read.shape[1]/n_gaps)
last_r_read = last_r_read.reshape(n_gaps, r_length)
# clip read_resistances to desired ranges
max_last_r_read_idx = np.full(maximum_r_read.shape,
                              last_r_read.shape[1]).astype(int)
if clip_r_read:
    for g_idx, g in enumerate(last_r_read):
        max_last_r_read_idx[g_idx] = int(np.argmax(g > maximum_r_read[g_idx]))

# Export computed data for Gnuplot printing
file = open(pre + 'simulated_read_resistance.data', 'w')
# for x_idx, x in enumerate(r_loads):
#         file.write(str(x) + ', ')
#         for r in last_r_read[:, x_idx]:
#                 file.write(str(r) + ', ')
#         file.write('\n')
for x_idx, x in enumerate(np.transpose(last_r_read)):
    file.write(str(r_loads[x_idx]))
    for r in x:
        file.write(', ' + str(r))
    file.write('\n')
file.close()

# Plot results
plot_2d = True
if plot_2d:
    data_read_r = []
    for g_idx, g in enumerate(last_r_read):
        data_read_r.append(
            plotly.graph_objs.Scatter(
                x=r_loads[0:max_last_r_read_idx[g_idx]],
                y=g[0:max_last_r_read_idx[g_idx]],
                mode='lines+markers',
                name='read_r for initial gap ' + str(initial_gaps[g_idx])
            )
        )
    layout_read_r = plotly.graph_objs.Layout(
        title=cell + ' Simulated Read Resistances vs Load Resistances',
        xaxis=dict(
            title='Load Resistance [ohm]',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#666666'
            )
        ),
        yaxis=dict(
            title='Read Resistance [ohm]',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#666666'
            )
        )
    )
    fig_read_r = plotly.graph_objs.Figure(data=data_read_r,
                                          layout=layout_read_r)
    plotly.offline.plot(fig_read_r, filename=pre + 'read_resistance.html')


##########################################################
# find the simulated resistance closer to de target value
##########################################################
sim_read_r = np.zeros([n_gaps, target_levels])
for g_idx, g in enumerate(last_r_read):
    sim_read_r[g_idx] = np.linspace(np.min(g[0:max_last_r_read_idx[g_idx]]),
                                    np.max(g[0:max_last_r_read_idx[g_idx]]),
                                    target_levels)

# required resistor loads
required_loads = np.zeros(sim_read_r.shape)
# simple 1:levels axysd
simple_index = np.linspace(1, target_levels, target_levels)

# export computed index
np.savetxt(pre + "simple_index_x.data",
           np.transpose(simple_index), delimiter=",")

# find target gaps for each target resistance
# at v_read [1:max_last_r_read_idx[g_idx]]
for g_idx, g in enumerate(sim_read_r):
    for t_idx, r in enumerate(g):
        new_r, r_idx = find_nearest_sorted(last_r_read[g_idx,
                                           0:max_last_r_read_idx[g_idx]], r)
        sim_read_r[g_idx, t_idx] = new_r
        required_loads[g_idx, t_idx] = r_loads[r_idx]

# Export computed data for Gnuplot printing
np.savetxt(pre + "ideal_load_resistances.data",
           np.transpose(required_loads), delimiter=",")
np.savetxt(pre + "ideal_read_r_for_load_resistances.data",
           np.transpose(sim_read_r), delimiter=",")

# plot results
if plot_2d:
    fig_r = plotly.tools.make_subplots(rows=1, cols=2, print_grid=False)

    for g_idx, g in enumerate(required_loads):
        fig_r.append_trace(
            plotly.graph_objs.Scatter(
                x=simple_index,
                y=g,
                mode='lines+markers',
                name='load_r for initial gap ' + str(initial_gaps[g_idx]),
                xaxis='x1',
                yaxis='y1'
            ), 1, 1)

        fig_r.append_trace(
            plotly.graph_objs.Scatter(
                x=simple_index,
                y=sim_read_r[g_idx, :],
                mode='lines+markers',
                name='read_r for initial gap ' + str(initial_gaps[g_idx]),
                xaxis='x2',
                yaxis='y2'
            ), 1, 2)

    layout_r = plotly.graph_objs.Layout(
        title=cell + ' Linearizing the ML-write function: quasilineal read_resistance.'
        '\nLoad Resistances and simulated Read Resistances for each level',
        xaxis1=dict(
            title='Level',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#666666'
            )
        ),
        xaxis2=dict(
            title='Level',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#666666'
            )
        ),
        yaxis1=dict(
            title='Load Resistance [ohm]',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#666666'
            )
        ),
        yaxis2=dict(
            title='Read Resistance [ohm]',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#666666'
            ),
            # side='right',
            # overlaying='y'
        )
    )
    fig_r.update(layout=layout_r)
    plotly.offline.plot(fig_r, filename=pre + 'load_resistances.html')

########################################################
# find read values if load resistors are equidistanced
########################################################
eq_distributed_loads = np.zeros(required_loads.shape)
for g_idx, g in enumerate(required_loads):
    eq_distributed_loads[g_idx] = np.append(
        np.linspace(g[0], g[g.shape[0]-2], target_levels-1), g[g.shape[0]-1])

# find the simulated read_resistance
# if loads are equidistanced (eq_d_)
eq_d_read_r = np.zeros(eq_distributed_loads.shape)
real_eq_d_loads = np.zeros(eq_distributed_loads.shape)

# read resistance
for g_idx, g in enumerate(eq_distributed_loads):
    for t_idx, r in enumerate(g):
        new_r, r_idx = find_nearest_sorted(r_loads, r)
        real_eq_d_loads[g_idx, t_idx] = new_r
        eq_d_read_r[g_idx, t_idx] = last_r_read[g_idx, r_idx]

# Export computed data for Gnuplot printing
np.savetxt(pre + "equidistanced_load_resistances.data",
           np.transpose(eq_distributed_loads), delimiter=",")
np.savetxt(pre + "equidistanced_read_r_for_load_resistances.data",
           np.transpose(eq_d_read_r), delimiter=",")

# plot
if plot_2d:
    fig_eq_l_r = plotly.tools.make_subplots(rows=1, cols=2, print_grid=False)

    for g_idx, g in enumerate(eq_distributed_loads):
        print('g_' + str(g_idx) + ' Initial HRS=' + str(eq_d_read_r[g_idx, 0]))
        fig_eq_l_r.append_trace(
            plotly.graph_objs.Scatter(
                x=simple_index,
                y=g,
                mode='lines+markers',
                name='load_r for initial gap ' + str(initial_gaps[g_idx]),
                xaxis='x1',
                yaxis='y1'
            ), 1, 1)

        fig_eq_l_r.append_trace(
            plotly.graph_objs.Scatter(
                x=simple_index,
                y=eq_d_read_r[g_idx, :],
                mode='lines+markers',
                name='read_r for initial gap ' + str(initial_gaps[g_idx]),
                xaxis='x2',
                yaxis='y2'
            ), 1, 2)

    layout_eq_l_r = plotly.graph_objs.Layout(
        title=cell + ' Linearizing the ML-write function: quasilineal read_resistance.'
        '\nEquidistanced Load Resistances and corresponding'
        'Read Resistances for each level',
        xaxis1=dict(
            title='Level',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#666666'
            )
        ),
        xaxis2=dict(
            title='Level',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#666666'
            )
        ),
        yaxis1=dict(
            title='Load Resistance [ohm]',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#666666'
            )
        ),
        yaxis2=dict(
            title='Read Resistance [ohm]',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#666666'
            ),
            # side='right',
            # overlaying='y'
        )
    )
    fig_eq_l_r.update(layout=layout_eq_l_r)
    plotly.offline.plot(fig_eq_l_r,
                        filename=pre + 'equidistanced_load_resistances.html')
