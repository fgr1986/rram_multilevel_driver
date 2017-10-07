
# coding: utf-8

# In[1]:


# import plotly.plotly as py
import plotly.offline
from plotly.graph_objs import Scatter, Layout
import numpy as np
import pandas as pd


# In[2]:


def find_nearest(array, value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]


def find_nearest_sorted(sorted_array, value):
    idx = np.searchsorted(sorted_array, value, side="left")
    if (idx > 0 and (
        idx == len(sorted_array)
        or math.fabs(value - sorted_array[idx-1])<math.fabs(value-sorted_array[idx]))):
        return sorted_array[idx-1], idx-1
    else:
        return sorted_array[idx], idx


# In[3]:


# Device parameters
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
v_read = 0.1 # already in voltages array, no interpolation needed
v_set = 1.8
v_write = 2*v_set
v_min = 0.1
v_step = 0.1
v_max = v_write
# target resistances
levels = 32
target_r = np.linspace(5e3, 1e6, levels)


# In[4]:


plot_3d = False
plot_r0 = True
plot_r_loads = True


# In[6]:


voltages_number = int((v_max - v_min)/v_step + 1)
gaps_number = 150
v_w = np.linspace(v_min, v_max, voltages_number)
gaps = np.linspace(p_gap_min, p_gap_max, gaps_number)
XX, YY = np.meshgrid(v_w, gaps)
v_w


# In[7]:


# idea
# r = v./(p_I0*exp(-g/p_g0)*sinh(v/p_V0))
#
# def resistance(v, g):
#     return v/(p_I0*math.exp(-g/p_g0)*math.sinh(v/p_V0))
# outer multiplication to get the NxN matrix
v_m = v_w
read_current = np.outer(p_I0*np.exp(-gaps/p_g0), np.sinh(v_m/p_V0))
# element wise division
eq_resistance = np.divide(v_m, read_current)




# In[12]:


# configure plotly
# creates .plotly/.config and ./plotly/.credentials

# plotly.tools.set_credentials_file(username='fmu', api_key='NIDiVLcNRVtwNzBnfpLJ')
plotly.tools.set_config_file(world_readable=False,
                             sharing='private')
# plotly.tools.set_config_file(world_readable=True,
#                            sharing='public')


# In[13]:


if plot_3d:
    data_3d = [
        plotly.graph_objs.Surface(
            x=XX,
            y=YY,
            z=eq_resistance,  # z_data.as_matrix(),
            name='RRAM resistance vs gap and voltage'
        )
    ]
    layout_3d = plotly.graph_objs.Layout(
        scene=plotly.graph_objs.Scene(
            xaxis=plotly.graph_objs.XAxis(title='x axis title'),
            yaxis=plotly.graph_objs.YAxis(title='y axis title'),
            zaxis=plotly.graph_objs.ZAxis(title='z axis title')
        ),
        title='Read resistance: gap vs read_voltage'
        # autosize=False,
        # width=500,
        # height=500,
        # margin=dict(
        #     l=65,
        #     r=50,
        #     b=65,
        #     t=90
        # )
    )
    fig = plotly.graph_objs.Figure(data=data_3d, layout=layout_3d)
    plotly.offline.plot(data_3d, filename = 'read_resistance_3d.html')


# In[14]:


# v_write / (r_m + r_s) = v_control/r_s
# r_m = f( gap, v_m ) = f( gap, v_write - v_control )

# find those v_m that guarantees
# read_current * r_s = v_w - v_m
v_w


# In[43]:


# read resistance for v=v_read
resistance_0 = eq_resistance[0:, 0]
closest_v, target_v_idx = find_nearest_sorted(voltages, v_read)
# update v_read
v_read = closest_v
resistance_0 = eq_resistance[0:, target_v_idx]

# find resistance for v=v_set
closest_v, target_v_idx = find_nearest_sorted(voltages, v_set)
# update v_set
v_set = closest_v
resistance_f = eq_resistance[0:, target_v_idx]

print('v_set: ' + str(v_set) + ' V')

# compute required resistances
req_resistances = np.zeros(levels)
for r_idx, r in enumerate(target_r):
    # get desired gap
    closest_r, target_g_idx = find_nearest_sorted(resistance_0, r)
    # update target_r
    req_resistances[r_idx] = resistance_f[target_g_idx]
    target_g = gaps[target_g_idx] # desired gap
    print('\ndesired gap:' + str(target_g) + '[m], '
          + 'related to \n\tv_read resistance ' + str(resistance_0[target_g_idx]) + ' [ohms]'
          + 'related to \n\tv_set resistance ' + str(resistance_f[target_g_idx]) + ' [ohms]')

# get exponential fit
# a, b = np.polyfit(gaps, np.log(resistance_0), 1)


# In[46]:


if plot_r0:
    data_r0 = [
        plotly.graph_objs.Scatter(
            x=gaps,
            y=resistance_0,
            mode='lines+markers',
            name='v_read_resistance'
        ),
        plotly.graph_objs.Scatter(
            x=gaps,
            y=resistance_f,
            mode='lines+markers',
            name='v_set_resistance'
        )
    ]

    layout_r0 = plotly.graph_objs.Layout(
        title='Resistances at v_set and v_read',
        xaxis=dict(
            title='Gap [m]',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='Resistance [ohm]',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig_r0 = plotly.graph_objs.Figure(data=data_r0, layout=layout_r0)
    plotly.offline.plot(fig_r0, filename = 'read_resistance.html')


# In[47]:


if plot_r_loads:
    data_r_loads = [
        plotly.graph_objs.Scatter(
            x=target_r,
            y=eq_resistance,
            mode='lines+markers',
            name='v_read_resistance'
        )
        # ,
        # plotly.graph_objs.Scatter(
        #         x=target_r,
        #         y=np.log(req_resistances),
        #         mode='lines+markers',
        #         name='LOG v_read_resistance'
        # )
    ]


    layout_r_loads = plotly.graph_objs.Layout(
        xaxis=dict(
            type='linear',
            autorange=True,
            title='Target Resistance [ohm]',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            type='linear',
            autorange=True,
            title='Load Resistance [ohm]',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )

    fig = plotly.graph_objs.Figure(data=data_r_loads, layout=layout_r_loads)
    plotly.offline.plot(fig, filename = 'load_resistance.html')


# In[15]:


# v_gate
plot_v_gate = True

if plot_v_gate:
    aux_x = np.linspace(0, 2*v_set, 200)
    a=100
    aux_y = 1/(1+np.exp(a*(aux_x-v_set)))
    data_v_gate = [
        plotly.graph_objs.Scatter(
            x=aux_x,
            y=aux_y,
            mode='lines+markers',
            name='v_gate'
        )
    ]

    plotly.offline.plot(data_v_gate, filename = 'v_gate.html')


# In[ ]:
