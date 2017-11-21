# import plotly.plotly as py
import plotly.offline
from plotly.graph_objs import Scatter, Layout
import numpy as np
import pandas as pd
import os

############################
# Parameters
############################
# To obtain the target resistances/resistive loads
# initial gaps defined in the netlists
initial_gaps = np.array([1.2e-9, 1.3e-9, 1.367e-9, 1.5e-9, 1.6e-9, 1.7e-9])
# data from ../stand_alone_simulations/resistive_controlled_scheme/results
print('\n\tPrinting data for every gap in ' + str(initial_gaps) + '\n\n')
cell = '1r'
g_idx = 2
print('\tCell type: ' + cell + ', g: ' + str(initial_gaps[g_idx]))

pre = 'exported_results_montecarlo/' + cell + '_g_' + str(g_idx) + '_'
clip_r_read = False
if clip_r_read:
    generated_files_folder = 'exported_results_montecarlo/clip_range_r_read/'
    pre = generated_files_folder + cell + '_g_' + str(g_idx) + '_'
    data_file = '../../cadence/results/mc_results/mc_clip_range_r_read/mc_' + cell + '_g_' + str(g_idx) + '_32l_last_r_read.csv'
else:
    generated_files_folder = 'exported_results_montecarlo/full_range_r_read/'
    pre = generated_files_folder + cell + '_g_' + str(g_idx) + '_'
    data_file = '../../cadence/results/mc_results/mc_full_resistance_range/mc_' + cell + '_g_' + str(g_idx) + '_32l_last_r_read.csv'

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
print('\tInput data shape (with headers): ' + str(full_data.shape))
# remove headers
full_data = full_data[1:]


############################
# r_read vs r_load
############################
levels = full_data.shape[0]
print('\tInput data shape (no headers): '+ str(full_data.shape))
# Plot results
plot_2d = True
if plot_2d:
    # data
    r_read_traces = []
    for l_idx, l in enumerate(full_data):
        r_read_traces.append(
            plotly.graph_objs.Histogram(
                x=full_data[l_idx, 1:],
                name='l_' + str(l_idx),
                opacity=0.75
            )
        )
    # layout
    layout = plotly.graph_objs.Layout(
        bargroupgap=0.3,
        barmode='overlay'
    )

    # layout = go.Layout(barmode='overlay')
    fig_read_r = plotly.graph_objs.Figure(data=r_read_traces,
                                          layout=layout)
    plotly.offline.plot(fig_read_r, filename=pre + 'histogram.html')




############################
# r_read vs r_load
############################
levels = full_data.shape[0]
# Plot results
plot_cdf = True
if plot_cdf:
    # data/r_
    r_read_traces = []
    cdf_data = []
    for l_idx, l in enumerate(full_data):
        # hist, bin_edges = np.histogram(full_data[l_idx, 1:], normed=True)
        # cumsum = np.cumsum(hist)
        
        sorted_data = np.sort(full_data[l_idx, 1:])
        y_vals=np.arange(len(sorted_data))/float(len(sorted_data)-1)
        cdf_data.append(sorted_data)
        cdf_data.append(y_vals)

        # add plotly trace
        r_read_traces.append(plotly.graph_objs.Scatter(
            x=sorted_data,
            y=y_vals,
            name='l_' + str(l_idx),
            )
        )
    # layout
    layout = plotly.graph_objs.Layout(
        # bargroupgap=0.3,
        # barmode='overlay'
    )

    # layout = go.Layout(barmode='overlay')
    fig_read_r = plotly.graph_objs.Figure(data=r_read_traces,
                                          layout=layout)
    plotly.offline.plot(fig_read_r, filename=pre + 'cdf.html')

# Export computed data for Gnuplot printing
np.savetxt(pre + "cdf.data",
           np.transpose(cdf_data), delimiter=",")
