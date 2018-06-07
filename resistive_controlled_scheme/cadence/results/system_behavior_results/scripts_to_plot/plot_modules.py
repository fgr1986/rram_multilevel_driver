import matplotlib.pyplot as plt
# import matplotlib.transforms as trn
from scipy import ndimage
import matplotlib.gridspec as gridspec
import numpy as np
import math

# columns

#################################################
# time (s)	clk (V)	start_op (V)	counter_0	fsm_0 (V)	fsm_1 (V)	EN_RESET (V)	EN_SET (V)	END_RESET (V)	V_WR (V)	ADD	V_RAW (V)	V_RESET (V)	V_SET (V)	V_LOAD (V)	V_SEL (V)	LEV	rram r read	rram cf temp	AC_0 (V)	AC_1 (V)	AC_2 (V)	AD_0 (V)	AD_1 (V)	AD_2 (V)	AS_0 (V)	AS_1 (V)	AS_2 (V)	AM_0 (V)	AM_1 (V)	AM_2 (V)	AM_3 (V)	AM_4 (V)	AM_5 (V)	AM_6 (V)	AM_7 (V)	AM_8 (V)	AM_9 (V)	AM_10 (V)	AM_11 (V)	AM_12 (V)	AM_13 (V)	AM_14 (V)	AM_15 (V)	AM_16 (V)	AM_17 (V)	AM_18 (V)	AM_19 (V)	AM_20 (V)	AM_21 (V)	AM_22 (V)	AM_23 (V)	AM_24 (V)	AM_25 (V)	AM_26 (V)	AM_27 (V)	AM_28 (V)	AM_29 (V)	AM_30 (V)	AM_31 (V)

#################################################

file_in = 'system_signals.csv'

# my_data = np.loadtxt(file_in, delimiter=',', skiprows=1)
my_data = np.loadtxt(file_in, delimiter=',', skiprows=1)
print(my_data.shape)
# 50001, 58

titles = np.genfromtxt(file_in, dtype=float,
                       delimiter=',', names=True).dtype.names

for t_idx, t in enumerate(titles):
    print(t_idx, ' ', t)
# print(my_data.shape)
# titles = my_data.dtype.names
# print(titles)
font = {'family': 'serif',
        # 'color':  'darkred',
        'weight': 'normal',
        # 'rotation:': 90,
        'size': 9,
        }

# scale data
rram_r = 17
my_data[:, 0] = my_data[:, 0] * 1e9
my_data[:, rram_r] = my_data[:, rram_r] * 1e-3

###########################################
# two stage write control
###########################################
# time (s)	clk (V)	start_op (V)	counter_0	fsm_0 (V)	fsm_1 (V)	EN_RESET (V)	EN_SET (V)

inputs_to_plot = [1, 2]
internal_to_plot = [3, 4, 5]
outputs_to_plot = [6, 7]
total_signals = inputs_to_plot + internal_to_plot + outputs_to_plot
print(total_signals)
plotted_columns = 1
plotted_rows = math.ceil(len(total_signals) / plotted_columns)

fig, axarr = plt.subplots(plotted_rows, plotted_columns,
                          sharex=True,
                          # figsize=(4, 8),
                          # dpi=300,
                          )

p_count = 0
for s in total_signals:

    c = int(np.floor((p_count) / plotted_rows))
    r = (p_count) % plotted_rows
    print('s:', s, 'r: ', r, 'c: ', c, ' ', titles[s])

    color_p = 'C0'
    if s in inputs_to_plot:
        color_p = 'darkgreen'
    elif s in internal_to_plot:
        color_p = 'gray'
    elif s in outputs_to_plot:
        color_p = 'darkorange'
    # if s==rram_r:
    #     ax = plt.subplot(gs[r:r+2, c])
    #     p_count += 1
    # else:
    #     ax = plt.subplot(gs[r, c])
        # ax.locator_params(axis='y', nbins=2)
    if c > 1:
        ax = axarr[r, c]
    else:
        ax = axarr[r]
    ax.plot(my_data[:, 0], my_data[:, s], color=color_p)
    # if subplot way
    # ax = axarr[r, c]
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    title = titles[s].replace('_V', " [V]")
    title = title.replace('rram_', "rram\n")
    title = title.replace('r_read', "r_read [KOhm]")
    title = title.replace('cf_temp', "CF temp [K]")
    ax.set_ylabel(title, fontdict=font, rotation='horizontal', labelpad=40)
    ax.grid(True)
    # if s >= resistive_mux_idx:
    #     ax.set_ylim([r_mux_min, r_mux_max])
    if (p_count) % plotted_rows == plotted_rows - 1:
        print('!!!!!!!!!!!!!time!!!!!!!!!!!!!!!!!!!!!!!!!')
        ax.set_xlabel('time [ns]', fontdict=font, rotation='horizontal')

    p_count += 1

# plt.figure(figsize=(10,20))
fig = plt.gcf()
fig.set_size_inches(5, 10)
fig.tight_layout()
fig.subplots_adjust(hspace=0.2)
fig.subplots_adjust(wspace=0.6)
# fig.tight_layout()
# fig.canvas.draw()
# fig.canvas.flush_events()

# mng = plt.get_current_fig_manager()
# # mng.frame.Maximize(True)
# mng.full_screen_toggle()


# Rotated_Plot = ndimage.rotate(fig, 90)
# plt.show(Rotated_Plot)

plt.savefig("two_stage_write_control.svg")
plt.savefig("two_stage_write_control.png")
# plt.show()
plt.close()


###########################################
# RRAM
###########################################
# time (s)	V_WR (V)	V_LOAD (V)	rram r read	rram cf temp

inputs_to_plot = [9, 14]
internal_to_plot = [17, 18]
outputs_to_plot = []
total_signals = inputs_to_plot + internal_to_plot + outputs_to_plot
print(total_signals)
plotted_columns = 1
plotted_rows = math.ceil(len(total_signals) / plotted_columns)

fig, axarr = plt.subplots(plotted_rows, plotted_columns,
                          sharex=True,
                          # figsize=(4, 8),
                          # dpi=300,
                          )

p_count = 0
for s in total_signals:

    c = int(np.floor((p_count) / plotted_rows))
    r = (p_count) % plotted_rows
    print('s:', s, 'r: ', r, 'c: ', c, ' ', titles[s])

    color_p = 'C0'
    if s in inputs_to_plot:
        color_p = 'darkgreen'
    elif s in internal_to_plot:
        color_p = 'gray'
    elif s in outputs_to_plot:
        color_p = 'darkorange'
    # if s==rram_r:
    #     ax = plt.subplot(gs[r:r+2, c])
    #     p_count += 1
    # else:
    #     ax = plt.subplot(gs[r, c])
        # ax.locator_params(axis='y', nbins=2)
    if c > 1:
        ax = axarr[r, c]
    else:
        ax = axarr[r]
    ax.plot(my_data[:, 0], my_data[:, s], color=color_p)
    # if subplot way
    # ax = axarr[r, c]
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    title = titles[s].replace('_V', " [V]")
    title = title.replace('rram_', "rram\n")
    title = title.replace('r_read', "r_read [KOhm]")
    title = title.replace('cf_temp', "CF temp [K]")
    ax.set_ylabel(title, fontdict=font, rotation='horizontal', labelpad=40)
    ax.grid(True)
    # if s >= resistive_mux_idx:
    #     ax.set_ylim([r_mux_min, r_mux_max])
    if (p_count) % plotted_rows == plotted_rows - 1:
        print('!!!!!!!!!!!!!time!!!!!!!!!!!!!!!!!!!!!!!!!')
        ax.set_xlabel('time [ns]', fontdict=font, rotation='horizontal')

    p_count += 1

# plt.figure(figsize=(10,20))
fig = plt.gcf()
fig.set_size_inches(5, 10)
fig.tight_layout()
fig.subplots_adjust(hspace=0.2)
fig.subplots_adjust(wspace=0.6)
# fig.tight_layout()
# fig.canvas.draw()
# fig.canvas.flush_events()

# mng = plt.get_current_fig_manager()
# # mng.frame.Maximize(True)
# mng.full_screen_toggle()


# Rotated_Plot = ndimage.rotate(fig, 90)
# plt.show(Rotated_Plot)

plt.savefig("rram_signals.svg")
plt.savefig("rram_signals.png")
# plt.show()
plt.close()

###########################################
# Crossbar Address Control
###########################################
# time (s)	V_WR (V)	ADD	V_LOAD (V)	V_SEL (V)	AC_0 (V)	AC_1 (V)	AC_2 (V)	AD_0 (V)	AD_1 (V)	AD_2 (V)	AS_0 (V)	AS_1 (V)	AS_2 (V)

inputs_to_plot = [9, 14, 10]
internal_to_plot = [15]
outputs_to_plot = list(range(19, 28))
total_signals = inputs_to_plot + internal_to_plot + outputs_to_plot
print(total_signals)
plotted_columns = 1
plotted_rows = math.ceil(len(total_signals) / plotted_columns)

fig, axarr = plt.subplots(plotted_rows, plotted_columns,
                          sharex=True,
                          # figsize=(4, 8),
                          # dpi=300,
                          )

p_count = 0
for s in total_signals:

    c = int(np.floor((p_count) / plotted_rows))
    r = (p_count) % plotted_rows
    print('s:', s, 'r: ', r, 'c: ', c, ' ', titles[s])

    color_p = 'C0'
    if s in inputs_to_plot:
        color_p = 'darkgreen'
    elif s in internal_to_plot:
        color_p = 'gray'
    elif s in outputs_to_plot:
        color_p = 'darkorange'
    # if s==rram_r:
    #     ax = plt.subplot(gs[r:r+2, c])
    #     p_count += 1
    # else:
    #     ax = plt.subplot(gs[r, c])
        # ax.locator_params(axis='y', nbins=2)
    if c > 1:
        ax = axarr[r, c]
    else:
        ax = axarr[r]
    ax.plot(my_data[:, 0], my_data[:, s], color=color_p)
    # if subplot way
    # ax = axarr[r, c]
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    title = titles[s].replace('_V', " [V]")
    title = title.replace('rram_', "rram\n")
    title = title.replace('r_read', "r_read [KOhm]")
    title = title.replace('cf_temp', "CF temp [K]")
    ax.set_ylabel(title, fontdict=font, rotation='horizontal', labelpad=40)
    ax.grid(True)
    # if s >= resistive_mux_idx:
    #     ax.set_ylim([r_mux_min, r_mux_max])
    if (p_count) % plotted_rows == plotted_rows - 1:
        print('!!!!!!!!!!!!!time!!!!!!!!!!!!!!!!!!!!!!!!!')
        ax.set_xlabel('time [ns]', fontdict=font, rotation='horizontal')

    p_count += 1

# plt.figure(figsize=(10,20))
fig = plt.gcf()
fig.set_size_inches(5, 10)
fig.tight_layout()
fig.subplots_adjust(hspace=0.2)
fig.subplots_adjust(wspace=0.6)
# fig.tight_layout()
# fig.canvas.draw()
# fig.canvas.flush_events()

# mng = plt.get_current_fig_manager()
# # mng.frame.Maximize(True)
# mng.full_screen_toggle()


# Rotated_Plot = ndimage.rotate(fig, 90)
# plt.show(Rotated_Plot)

plt.savefig("crossbar_addr.svg")
plt.savefig("crossbar_addr.png")
# plt.show()
plt.close()


###########################################
# Voltage Current Control
###########################################
# time (s)	EN_RESET (V)	EN_SET (V)	END_RESET (V)	V_RAW (V)	V_RESET (V)	V_SET (V)	V_WR (V)

inputs_to_plot = [6, 7, 8, 11]
internal_to_plot = [12, 13]
outputs_to_plot = [9]
total_signals = inputs_to_plot + internal_to_plot + outputs_to_plot
print(total_signals)
plotted_columns = 1
plotted_rows = math.ceil(len(total_signals) / plotted_columns)

fig, axarr = plt.subplots(plotted_rows, plotted_columns,
                          sharex=True,
                          # figsize=(4, 8),
                          # dpi=300,
                          )

p_count = 0
for s in total_signals:

    c = int(np.floor((p_count) / plotted_rows))
    r = (p_count) % plotted_rows
    print('s:', s, 'r: ', r, 'c: ', c, ' ', titles[s])

    color_p = 'C0'
    if s in inputs_to_plot:
        color_p = 'darkgreen'
    elif s in internal_to_plot:
        color_p = 'gray'
    elif s in outputs_to_plot:
        color_p = 'darkorange'
    # if s==rram_r:
    #     ax = plt.subplot(gs[r:r+2, c])
    #     p_count += 1
    # else:
    #     ax = plt.subplot(gs[r, c])
        # ax.locator_params(axis='y', nbins=2)
    if c > 1:
        ax = axarr[r, c]
    else:
        ax = axarr[r]
    ax.plot(my_data[:, 0], my_data[:, s], color=color_p)
    # if subplot way
    # ax = axarr[r, c]
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    title = titles[s].replace('_V', " [V]")
    title = title.replace('rram_', "rram\n")
    title = title.replace('r_read', "r_read [KOhm]")
    title = title.replace('cf_temp', "CF temp [K]")
    ax.set_ylabel(title, fontdict=font, rotation='horizontal', labelpad=40)
    ax.grid(True)
    # if s >= resistive_mux_idx:
    #     ax.set_ylim([r_mux_min, r_mux_max])
    if (p_count) % plotted_rows == plotted_rows - 1:
        print('!!!!!!!!!!!!!time!!!!!!!!!!!!!!!!!!!!!!!!!')
        ax.set_xlabel('time [ns]', fontdict=font, rotation='horizontal')

    p_count += 1

# plt.figure(figsize=(10,20))
fig = plt.gcf()
fig.set_size_inches(5, 10)
fig.tight_layout()
fig.subplots_adjust(hspace=0.2)
fig.subplots_adjust(wspace=0.6)
# fig.tight_layout()
# fig.canvas.draw()
# fig.canvas.flush_events()

# mng = plt.get_current_fig_manager()
# # mng.frame.Maximize(True)
# mng.full_screen_toggle()


# Rotated_Plot = ndimage.rotate(fig, 90)
# plt.show(Rotated_Plot)

plt.savefig("voltage_current_control.svg")
plt.savefig("voltage_current_control.png")
# plt.show()
plt.close()


###########################################
# R_loads / A.Mux
###########################################
# time (s)	EN_RESET (V)	EN_SET (V)	V_LOAD (V)	LEV	AM_0 (V)	AM_1 (V)	AM_2 (V)	AM_3 (V)	AM_4 (V)	AM_5 (V)	AM_6 (V)	AM_7 (V)	AM_8 (V)	AM_9 (V)	AM_10 (V)	AM_11 (V)	AM_12 (V)	AM_13 (V)	AM_14 (V)	AM_15 (V)	AM_16 (V)	AM_17 (V)	AM_18 (V)	AM_19 (V)	AM_20 (V)	AM_21 (V)	AM_22 (V)	AM_23 (V)	AM_24 (V)	AM_25 (V)	AM_26 (V)	AM_27 (V)	AM_28 (V)	AM_29 (V)	AM_30 (V)	AM_31 (V)


inputs_to_plot = [6, 7, 14, 16]
internal_to_plot = []
outputs_to_plot = list(range(28, 60))
total_signals = inputs_to_plot + internal_to_plot + outputs_to_plot
print(total_signals)
plotted_columns = 2
plotted_rows = math.ceil(len(total_signals) / plotted_columns)

fig, axarr = plt.subplots(plotted_rows, plotted_columns,
                          sharex=True,
                          # figsize=(4, 8),
                          # dpi=300,
                          )

p_count = 0
for s in total_signals:

    c = int(np.floor((p_count) / plotted_rows))
    r = (p_count) % plotted_rows
    print('s:', s, 'r: ', r, 'c: ', c, ' ', titles[s])

    color_p = 'C0'
    if s in inputs_to_plot:
        color_p = 'darkgreen'
    elif s in internal_to_plot:
        color_p = 'gray'
    elif s in outputs_to_plot:
        color_p = 'darkorange'
    # if s==rram_r:
    #     ax = plt.subplot(gs[r:r+2, c])
    #     p_count += 1
    # else:
    #     ax = plt.subplot(gs[r, c])
        # ax.locator_params(axis='y', nbins=2)
    if plotted_columns > 1:
        ax = axarr[r, c]
    else:
        ax = axarr[r]
    ax.plot(my_data[:, 0], my_data[:, s], color=color_p)
    # if subplot way
    # ax = axarr[r, c]
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    title = titles[s].replace('_V', " [V]")
    title = title.replace('rram_', "rram\n")
    title = title.replace('r_read', "r_read [KOhm]")
    title = title.replace('cf_temp', "CF temp [K]")
    ax.set_ylabel(title, fontdict=font, rotation='horizontal', labelpad=40)
    ax.grid(True)
    # if s >= resistive_mux_idx:
    #     ax.set_ylim([r_mux_min, r_mux_max])
    if (p_count) % plotted_rows == plotted_rows - 1:
        print('!!!!!!!!!!!!!time!!!!!!!!!!!!!!!!!!!!!!!!!')
        ax.set_xlabel('time [ns]', fontdict=font, rotation='horizontal')

    p_count += 1

# plt.figure(figsize=(10,20))
fig = plt.gcf()
fig.set_size_inches(8, 10)
fig.tight_layout()
fig.subplots_adjust(hspace=0.2)
fig.subplots_adjust(wspace=0.6)
# fig.tight_layout()
# fig.canvas.draw()
# fig.canvas.flush_events()

# mng = plt.get_current_fig_manager()
# # mng.frame.Maximize(True)
# mng.full_screen_toggle()


# Rotated_Plot = ndimage.rotate(fig, 90)
# plt.show(Rotated_Plot)

plt.savefig("rloads.svg")
plt.savefig("rloads.png")
# plt.show()
plt.close()
