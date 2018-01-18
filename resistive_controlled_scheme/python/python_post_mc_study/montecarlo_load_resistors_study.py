# import plotly.plotly as py
import plotly.offline
import matplotlib.pyplot as plt

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
cell = '1t1r'
r_range = 'full_range'
# r_range = 'clip_range'
experiment = 'only_intra_device_variability' # to the date, 500 MC
experiment = 'inter_intra_device_variability' # to the date 1e3 MC

# exported from spectre using oceanExport
base_cadence_results_folder = '../../cadence/results/mc_results/'
crf = base_cadence_results_folder + experiment + '/' + r_range + '/'
exp_folder = 'exported_results_montecarlo/' + experiment + '/' + r_range + '/'
levels = 32
# mc_sims = 500
mc_sims = 1000
selected_levels = np.array(np.linspace(0,31,32))
for g_idx in np.arange(initial_gaps.shape[0]):
    print('\tCell type: ' + cell + ', g: ' + str(initial_gaps[g_idx]))

    pre = exp_folder + cell + '_g_' + str(g_idx) + '_'
    generated_files_folder = pre + '/'
    data_file = crf + 'mc_' + cell + '_g_' + str(g_idx) + '/mc_data'
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
    # format: 1 column of M_mc X L_levels
    # level_0_m_0_r_read, ....
    # level_1_m_0_r_read, ...
    # level_N-1_m_0_r_read, .....
    # level_0_m_1_r_read, ....
    full_data = np.genfromtxt(data_file)
    # reshape towards a LxMC matrix
    full_data = np.reshape(full_data, (levels, mc_sims), order='F')

    #############################
    # r_read vs r_load histogram
    #############################
    print('\tInput data shape (no headers): ' + str(full_data.shape))
    # Plot results
    plot_hist = True
    plot_matplotlib = False
    if plot_hist:
        # data
        r_read_traces = []
        for l_idx, l in enumerate(full_data):
            if l_idx in selected_levels:
                # full_data[l_idx, 1] is an integer with the level
                r_read_traces.append(
                    plotly.graph_objs.Histogram(
                        x=l,  # full_data[l_idx, 1:],
                        name='l_' + str(l_idx),
                        opacity=0.75
                    )
                )
                if plot_matplotlib:
                    plt.hist(l)
                    plt.xlabel('Read Resistance at 0.1V [KOhms]')
                    plt.ylabel('# of occurrences')
        if plot_matplotlib:
            plt.show()
        # layout
        layout = plotly.graph_objs.Layout(
            bargroupgap=0.3,
            barmode='overlay'
        )

        # layout = go.Layout(barmode='overlay')
        fig_read_r = plotly.graph_objs.Figure(data=r_read_traces,
                                              layout=layout)
        plotly.offline.plot(fig_read_r, filename=pre + 'histogram.html')

    # Export computed data for Gnuplot printing
    np.savetxt(pre + "raw.data",
               np.transpose(full_data), delimiter=",")

    ############################
    # r_read vs r_load cdf
    ############################
    levels = full_data.shape[0]
    # Plot results
    plot_cdf = False
    if plot_cdf:
        # data/r_
        r_read_traces = []
        cdf_data = []
        for l_idx, l in enumerate(full_data):
            sorted_data = np.sort(l)  # np.sort(full_data[l_idx, 1:])
            y_vals = np.arange(len(sorted_data))/float(len(sorted_data)-1)
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
