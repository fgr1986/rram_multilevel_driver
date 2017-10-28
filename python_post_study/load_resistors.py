# import plotly.plotly as py
import plotly.offline
from plotly.graph_objs import Scatter, Layout
import numpy as np
import pandas as pd

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
# target resistances
initial_gaps = np.array([1.3e-9, 1.367e-9, 1.5e-9, 1.6e-9, 1.7e-9])
data_file = 'exported_data/1t1r_last.csv'
n_gaps = initial_gaps.shape[0]
simulated_levels = 256
target_levels = 32
r_load_min = 1e3
r_loads = np.linspace(r_load_min,
                      simulated_levels*r_load_min, simulated_levels)

############################
# Plotly configuration
############################
plotly.tools.set_config_file(world_readable=False,
                             sharing='private')

############################
# Import data
############################
full_data = np.genfromtxt(data_file, delimiter=',')
# data in X0 Y0, X1, Y1 format, grab all Y values
last_r_read = np.array([full_data[full_data.shape[0]-1, 1::2]])
r_length = int(last_r_read.shape[1]/n_gaps)
last_r_read = last_r_read.reshape(n_gaps, r_length)

############################
# Plot results
############################
plot_2d = True
if plot_2d:
    data_read_r = []
    for g_idx, g in enumerate(last_r_read):
        data_read_r.append(
            plotly.graph_objs.Scatter(
                x=r_loads,
                y=g,
                mode='lines+markers',
                name='read_r for initial gap ' + str(initial_gaps[g_idx])
            )
        )
    layout_read_r = plotly.graph_objs.Layout(
        title='Simulated Read Resistances vs Load Resistances',
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
    plotly.offline.plot(fig_read_r, filename='read_resistance.html')

##########################################################
# find the simulated resistance closer to de target value
##########################################################
sim_read_r = np.zeros([n_gaps, target_levels])
for g_idx, g in enumerate(last_r_read):
    sim_read_r[g_idx] = np.linspace(np.min(g), np.max(g), target_levels)

# required resistor loads
required_loads = np.zeros(sim_read_r.shape)
# simple 1:levels axysd
simple_index = np.linspace(1, target_levels, target_levels)

# find target gaps for each target resistance at v_read
for g_idx, g in enumerate(sim_read_r):
    for t_idx, r in enumerate(g):
        new_r, r_idx = find_nearest_sorted(last_r_read[g_idx, :], r)
        sim_read_r[g_idx, t_idx] = new_r
        required_loads[g_idx, t_idx] = r_loads[r_idx]

# plot results
if plot_2d:
    fig_r = plotly.tools.make_subplots(rows=1, cols=2)

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
        title='Linearizing the ML-write function: quasilineal read_resistance.'
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
    plotly.offline.plot(fig_r, filename='load_resistances.html')

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
print(required_loads.shape)
for g_idx, g in enumerate(eq_distributed_loads):
    for t_idx, r in enumerate(g):
        new_r, r_idx = find_nearest_sorted(r_loads, r)
        real_eq_d_loads[g_idx, t_idx] = new_r
        eq_d_read_r[g_idx, t_idx] = last_r_read[g_idx, r_idx]

# plot
if plot_2d:
    fig_eq_l_r = plotly.tools.make_subplots(rows=1, cols=2)

    for g_idx, g in enumerate(eq_distributed_loads):
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
                y=eq_d_read_r[g_idx,:],
                mode='lines+markers',
                name='read_r for initial gap ' + str(initial_gaps[g_idx]),
                xaxis='x2',
                yaxis='y2'
            ), 1, 2)

    layout_eq_l_r = plotly.graph_objs.Layout(
        title='Linearizing the ML-write function: quasilineal read_resistance.'
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
                        filename='equidistanced_load_resistances.html')
