import matplotlib.pyplot as plt
# import matplotlib.transforms as trn
from scipy import ndimage
import matplotlib.gridspec as gridspec
import numpy as np

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
# print(my_data.shape)
# titles = my_data.dtype.names
# print(titles)
font = {'family': 'serif',
        # 'color':  'darkred',
        'weight': 'normal',
        # 'rotation:': 90,
        'size': 9,
        }
# hardcoded, seeing the printed output
rram_columns = np.array([17, 18])
rram_r = 17
mux_columns = np.array(list(range(19, 59)))
integer_columns = np.array([10, 16, 3])
resistive_mux_idx = 19
sel_idx = 15

r_mux_max = np.max(my_data[:, resistive_mux_idx+1:])
r_mux_min = np.min(my_data[:, resistive_mux_idx+1:])
print('r_mux_max:', r_mux_max)
print('r_mux_min:', r_mux_min)
# scale data
my_data[:, 0] = my_data[:, 0] * 1e9
my_data[:, rram_r] = my_data[:, rram_r] * 1e-3

#
total_signals = my_data.shape[1] - 1
plotted_columns = 2
plotted_rows = int(total_signals / plotted_columns)
height_ratios=np.ones(total_signals-2)
height_ratios[rram_r] = 2
print('total_signals:', total_signals)
print('plotted_rows:', plotted_rows)
print('plotted_columns:', plotted_columns)

gs = gridspec.GridSpec(plotted_rows, plotted_columns)

# fig, axarr = plt.subplots(plotted_rows, plotted_columns,
#                           sharex=True,
#                           # figsize=(4, 8),
#                           # dpi=300,
#                           )
p_count = 0
for s in range(1, total_signals):

    c = int(np.floor((p_count) / plotted_rows))
    r = (p_count) % plotted_rows
    print('s:', s, 'r: ', r, 'c: ', c, ' ', titles[s])
    if s == sel_idx:
        continue

    color_p = 'C0'
    if s in rram_columns:
        color_p = 'C1'
    elif s in mux_columns:
        color_p = 'C2'
    elif s in integer_columns:
        color_p = 'C3'
    if s==rram_r:
        ax = plt.subplot(gs[r:r+2, c])
        p_count += 1
    else:
        ax = plt.subplot(gs[r, c])
        # ax.locator_params(axis='y', nbins=2)
    ax.plot(my_data[:, 0], my_data[:, s], color=color_p)
    # if subplot way
    # ax = axarr[r, c]

    # ax.setp(ax2.get_xticklabels(), visible=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    # ax.spines["bottom"].set_visible(False)
    title = titles[s].replace('_V', " [V]")
    title = title.replace('rram_', "rram\n")
    title = title.replace('r_read', "r_read [KOhm]")
    title = title.replace('cf_temp', "CF temp [K]")
    ax.set_ylabel(title, fontdict=font, rotation='horizontal', labelpad=40)
    ax.grid(True)
    # if s in rram_columns:
        # ax.ticklabel_format(style='sci', axis='y')
    if s >= resistive_mux_idx:
        ax.set_ylim([r_mux_min, r_mux_max])
    if (p_count) % plotted_rows == plotted_rows-1:
        print('!!!!!!!!!!!!!time!!!!!!!!!!!!!!!!!!!!!!!!!')
        ax.set_xlabel('time [ns]', fontdict=font, rotation='horizontal')
    else:
        print('(p_count+1): ', (p_count+1), ' (p_count+1) % plotted_rows: ', (p_count+1) % plotted_rows)
        ax.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=False) # labels along the bottom edge are off

    p_count += 1

# plt.figure(figsize=(10,20))
fig = plt.gcf()
fig.set_size_inches(15, 22)
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

plt.savefig("system_signals_behavior.svg")
plt.savefig("system_signals_behavior.png")
# plt.show()
plt.close()

#################################################
