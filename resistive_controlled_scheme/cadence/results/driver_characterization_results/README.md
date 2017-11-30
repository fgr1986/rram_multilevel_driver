# Nominal Results
Last read resistances and transients for 1R and 1T1R.
Characteristics:
* 1024 levels (MLC)
* v_w=2x1.8V
* min p_r0=0.25k
* CF gaps: [1.2e-9, 1.3e-9, 1.367e-9, 1.5e-9, 1.6e-9, 1.7e-9]

Therefore the transient files contains:
* 6 cells (g_0-g_5), each with different gaps
* 1024 levels for each cell
* data is, by colums: X, g_0_r_read_level_0, X, g_0_r_read_level_1...., g_1_r_read_level_0...
