# import plotly.plotly as py
import plotly.offline
from plotly.graph_objs import Scatter, Layout
import numpy as np
import pandas as pd

############################
# Parameters
############################
# To obtain the target resistances/resistive loads
# initial gaps defined in the netlists
initial_gaps = np.array([1.3e-9, 1.367e-9, 1.5e-9, 1.6e-9, 1.7e-9])
# data from ../stand_alone_simulations/resistive_controlled_scheme/results
print('\n\tPrinting data for every gap in ' + str(initial_gaps) + '\n\n')
cell = '1r'
g_idx = 4
print('\tCell type: ' + cell + ', g: ' + str(initial_gaps[g_idx]))
pre = 'exported_results_montecarlo/' + cell + '_g_' + str(g_idx) + '_'
data_file = 'imported_data_montecarlo/mc_' + cell + '_g_' + str(g_idx) + '_32l_last_r_read.csv'

############################
# Plotly configuration
############################
plotly.tools.set_config_file(world_readable=False,
                             sharing='private')

############################
# Import data
############################
full_data = np.genfromtxt(data_file, delimiter=',')
print(full_data.shape)
# remove headers
full_data = full_data[1:]
# full_data = full_data[1::2]


############################
# r_read vs r_load
############################
levels = full_data.shape[0]
print(full_data.shape)
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
