# coding: utf-8


# import plotly.plotly as py
import plotly.offline
from plotly.graph_objs import Scatter, Layout
import numpy as np
import pandas as pd
import os

# constants
p_kb = 1.3806503e-23 # Boltzmann's constant (J/K)
p_q = 1.6e-19  # electron charge(C)

# Device parameters
# taken from stanford's model
p_Rth = 2e5 # 5e5  # unit: K/W   effective thermal resistance
# arizona's model
# p_tstep = 5e-12 #for temp
# p_Rth = p_tstep/3.1825e-16 # unit: K/W
p_L = 5e-9   # from (0:inf); # Oxide thickness (m)
p_gap_min = 0.1e-9   # from (0:L); # Min. gap distance (m)
p_gap_max = 1.7e-9   # from (gap_min:L); # Max. gap distance (m)
p_gap_ini = 0.1e-9   # from [gap_min:gap_max];# Initial gap distance (m)
p_a0 = 0.25e-9   # from (0:inf); # Atomic distance (m)
p_Eag = 1.501   # from (0:inf); # Activation energy for vacancy generation (eV)
p_Ear = 1.5   # from (0:inf); # Activation energy for vac. recombination (eV)

# I-V characteristics
p_I0 = 6.14e-5   # from (0:inf);
p_g0 = 2.7505e-10   # from (0:inf);
p_V0 = 0.43   # from (0:inf);

# Gap dynamics
p_Vel0 = 150   # from (0:inf);
p_gamma0 = 16.5   # from (0:inf);
p_g1 = 1e-9   # from (0:inf);
p_beta = 1.25   # from (0:gamma0/(pow(gap_max/g1,3)));

# Temperature dynamics
p_T0 = 273+25   # from (0:inf);# Ambient temperature (K)
p_Cth = 3.1825e-16   # from (0:inf);# Effective thermal capacitance (J/K)
p_Tau_th = 2.3e-10   # from (0:inf);# Effective thermal time constant (s)

# Voltage parameters
v_read = 0.1  # already in voltages array, no interpolation needed
v_set = 1.8
v_write = 2*v_set
v_min = 0.1
v_max = v_write
# target resistances
levels = 32
target_r = np.linspace(10e3, 1e6, levels)
compatible_r = target_r
# grid
# g_step = 1e-12
# v_step = 1e-1
g_step = 1e-11
v_step = 1e-2

###################
# plot Parameters
###################
plot_3d_r = False
plot_3d_g = False
# configure plotly
# creates .plotly/.config and ./plotly/.credentials

plotly.tools.set_config_file(world_readable=False,
                             sharing='private')
# plotly.tools.set_config_file(world_readable=True,
#                            sharing='public')

expo = 'exported_data/'
export_temp_dep = False
voltages_number = int((v_max - v_min)/v_step + 1)
gaps_number = int((p_gap_max - p_gap_min)/g_step + 1)
v_m = np.array([np.linspace(v_min, v_max, voltages_number)])
gaps = np.array([np.linspace(p_gap_min, p_gap_max, gaps_number)])
XX, YY = np.meshgrid(v_m, gaps)
print('v_m shape: ' + str(v_m.shape))
print('gaps shape: ' + str(gaps.shape))
print('XX shape: ' + str(XX.shape))
print('YY shape: ' + str(YY.shape))

############################
# preparing folder
############################
# create final folder
if not os.path.exists(expo):
    os.makedirs(expo)

##################################
# current and resistances
##################################
print('------------------------------')
print('- 2D-Data structures:        -')
print('-   rows:    gaps            -')
print('-   columns: voltages        -')
print('------------------------------')
print('\n\n')
#
# idea
# r = v./(p_I0*exp(-g/p_g0)*sinh(v/p_V0))
#
# def resistance(v, g):
#     return v/(p_I0*math.exp(-g/p_g0)*math.sinh(v/p_V0))
# with outer
# eq_current_outer = np.outer(p_I0*np.exp(-gaps/p_g0), np.sinh(v_m/p_V0))

# with elemtn wise matrix like multiplication
# eq_current = (np.sinh(v_m/p_V0).T * p_I0*np.exp(-gaps/p_g0)).T
# with matrix like multiplication
eq_current = np.dot(np.sinh(v_m/p_V0).T, p_I0*np.exp(-gaps/p_g0)).T
# print('eq_current shape: ' + str(eq_current.shape))

# print(eq_current-eq_current_2)
# element wise division
# eq_resistance = np.divide(v_m, eq_current.T).T
eq_resistance = np.divide(v_m, eq_current)
print('eq_resistance shape: ' + str(eq_resistance.shape))


if plot_3d_r:
    data_3d_r = [
        plotly.graph_objs.Surface(
            x=XX,
            y=YY,
            z=eq_resistance,  # z_data.as_matrix(),
            name='RRAM resistance vs gap and voltage'
        )
    ]
    layout_3d_r = plotly.graph_objs.Layout(
        scene=plotly.graph_objs.Scene(
            xaxis=plotly.graph_objs.XAxis(title='applied voltage [V]'),
            yaxis=plotly.graph_objs.YAxis(title='gap [m]'),
            zaxis=plotly.graph_objs.ZAxis(title='equivalent resistance [ohm]')
        ),
        title='Read resistance: gap vs read_voltage'
    )
    fig_r = plotly.graph_objs.Figure(data=data_3d_r, layout=layout_3d_r)
    plotly.offline.plot(fig_r, filename=expo + 'read_resistance_3d.html')

    data_3d_i = [
        plotly.graph_objs.Surface(
            x=XX,
            y=YY,
            z=eq_current,  # z_data.as_matrix(),
            name='RRAM current vs gap and voltage'
        )
    ]
    layout_3d_i = plotly.graph_objs.Layout(
        title='RRAM current: gap vs read_voltage'
    )
    fig_i = plotly.graph_objs.Figure(data=data_3d_i, layout=layout_3d_i)
    plotly.offline.plot(fig_i, filename=expo + 'eq_current_3d.html')


#################
# gap study:
#################
#
# Formula:
# gap_ddt = -Vel0*( exp(-q*Eag/kb/temperature)*exp(gamma*a0/L*q*V(Nt,Nb)/kb/temperature) - exp(-q*Ear/kb/temperature)*exp(-gamma*a0/L*q*V(Nt,Nb)/kb/temperature) );

##################################
# gap_ddt temperature constant
##################################
temperature = p_T0
gamma = p_gamma0 - p_beta*np.power(gaps/p_g1, 3)
print('gamma shape: ' + str(gamma.shape))
gap_aux_1 = np.exp(-p_q*p_Eag/p_kb/temperature)
gap_1 = gap_aux_1*np.exp(np.dot(gamma.T, v_m*p_a0/p_L*p_q/p_kb/temperature ) )
gap_2 = gap_aux_1*np.exp(np.dot(-gamma.T, v_m*p_a0/p_L*p_q/p_kb/temperature ) )
gap_ddt = -p_Vel0*(gap_1 - gap_2)
gap_ddt_th = 1e6  #float("inf") #2500
gap_ddt[gap_ddt > gap_ddt_th] = gap_ddt_th
gap_ddt[gap_ddt < -gap_ddt_th] = -gap_ddt_th
print('gap_ddt shape: ' + str(gap_ddt.shape))

if plot_3d_g:

    data_3d_gddt = [
        plotly.graph_objs.Surface(
            x=XX,
            y=YY,
            z=gap_ddt,  # z_data.as_matrix(),
            name='gap_ddt with temp constant'
        )
    ]
    layout_3d_gddt = plotly.graph_objs.Layout(
        scene=plotly.graph_objs.Scene(
            xaxis=plotly.graph_objs.XAxis(title='applied voltage [V]'),
            yaxis=plotly.graph_objs.YAxis(title='gap [m]'),
            zaxis=plotly.graph_objs.ZAxis(title='temperature [K]')
        ),
        title='gap_ddt with temp constant: gap vs read_voltage'
    )
    fig_gddt = plotly.graph_objs.Figure(data=data_3d_gddt, layout=layout_3d_gddt)
    plotly.offline.plot(fig_gddt, filename = expo + 'gap_ddt.html')


###########################
# gap_ddt temp dependent
###########################
#
# gap_ddt = -Vel0*( exp(-q*Eag/kb/temperature)*exp(gamma*a0/L*q*V(Nt,Nb)/kb/temperature) - exp(-q*Ear/kb/temperature)*exp(-gamma*a0/L*q*V(Nt,Nb)/kb/temperature) );

# element wise
# temperature = p_T0 + abs( np.multiply(v_m.T, eq_current.T).T )* p_Rth
temperature = p_T0 + abs( v_m * eq_current )* p_Rth
gamma = p_gamma0 - p_beta*np.power(gaps/p_g1, 3)
print('temperature shape: ' + str(temperature.shape))
print('gamma shape: ' + str(gamma.shape))

if plot_3d_g:

    data_3d_t = [
        plotly.graph_objs.Surface(
            x=XX,
            y=YY,
            z=temperature,  # z_data.as_matrix(),
            name='temperature'
        )
    ]
    layout_3d_t = plotly.graph_objs.Layout(
        scene=plotly.graph_objs.Scene(
            xaxis=plotly.graph_objs.XAxis(title='applied voltage [V]'),
            yaxis=plotly.graph_objs.YAxis(title='gap [m]'),
            zaxis=plotly.graph_objs.ZAxis(title='temperature [K]')
        ),
        title='temperature: gap vs read_voltage'
    )
    fig_t = plotly.graph_objs.Figure(data=data_3d_t, layout=layout_3d_t)
    plotly.offline.plot(fig_t, filename = expo + 'temperature.html')

gap_ddt_aux_1 = np.exp(-p_q*p_Eag/p_kb/temperature)
print('gap_ddt_aux_1 shape: ' + str(gap_ddt_aux_1.shape))
gap_ddt_aux_2 = np.outer(gamma, v_m)*p_a0/p_L*p_q/p_kb  # with outer
# gap_ddt_aux_2 = (np.array([gamma]).T * np.array([v_m])).T *p_a0/p_L*p_q/p_kb
print('gap_ddt_aux_2 shape: ' + str(gap_ddt_aux_2.shape))
gap_ddt_aux_3 = np.exp( np.divide(  gap_ddt_aux_2, temperature ) )
# print('gap_ddt_aux_3 shape: ' + str(gap_ddt_aux_3.shape))
gap_ddt_aux_4 = np.exp( np.divide(  -gap_ddt_aux_2, temperature ) )
# print('gap_ddt_aux_4 shape: ' + str(gap_ddt_aux_4.shape))
gap_1 = np.multiply(gap_ddt_aux_1, gap_ddt_aux_3)
gap_2 = np.multiply(gap_ddt_aux_1,gap_ddt_aux_4)
gap_ddt_2 = -p_Vel0*( gap_1 - gap_2 )
# filter
gap_ddt_th = 2500
gap_ddt_2[gap_ddt_2 > gap_ddt_th] = gap_ddt_th
gap_ddt_2[gap_ddt_2 < -gap_ddt_th] = -gap_ddt_th
print('gap_ddt_2 shape: ' + str(gap_ddt_2.shape))

if plot_3d_g:

    data_3d_t = [
        plotly.graph_objs.Surface(
            x=XX,
            y=YY,
            z=gap_ddt_2,  # z_data.as_matrix(),
            name='gap_ddt_2 (variable temperature)'
        )
    ]
    layout_3d_t = plotly.graph_objs.Layout(
        scene=plotly.graph_objs.Scene(
            xaxis=plotly.graph_objs.XAxis(title='applied voltage [V]'),
            yaxis=plotly.graph_objs.YAxis(title='gap [m]'),
            zaxis=plotly.graph_objs.ZAxis(title='temperature [K]')
        ),
        title='gap_ddt_2 (variable temperature): gap vs read_voltage'
    )
    fig_t = plotly.graph_objs.Figure(data=data_3d_t, layout=layout_3d_t)
    plotly.offline.plot(fig_t, filename = expo + 'gap_ddt_2.html')

if export_temp_dep:
    # only 3d data
    np.savetxt(expo + 'gap_ddt2.csv', gap_ddt_2, delimiter=',')
    # for gnuplot
    file = open(expo + 'gap_ddt2.data', 'w')
    y_decim = 3
    x_decim = 5
    for y_idx, y in enumerate(v_m[0, ::y_decim]):
            for x_idx, x in enumerate(gaps[0, ::x_decim]):
                    file.write(str(y) + ' ' + str(x) + ' ' +
                               str(gap_ddt_2[x_idx*x_decim, y_idx*y_decim]) +
                               '\n')
            file.write('\n')
    file.close()
else:
    # only 3d data
    np.savetxt(expo + 'gap_ddt.csv', gap_ddt, delimiter=',')
    # for gnuplot
    file = open(expo + 'gap_ddt.data', 'w')
    y_decim = 3
    x_decim = 5
    for y_idx, y in enumerate(v_m[0, ::y_decim]):
            for x_idx, x in enumerate(gaps[0, ::x_decim]):
                    file.write(str(y) + ' ' + str(x) + ' ' +
                               str(gap_ddt[x_idx * x_decim, y_idx * y_decim]) +
                               '\n')
            file.write('\n')

    file.close()
