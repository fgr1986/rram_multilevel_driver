# rram_multilevel_driver
Architecture for RRAM multilevel programming

## Description
The present framework provides the circuit designer with the design
and software tools to ensure the reliable programming of MLC RRAMs.

Valid for both 1T1R and 1R schemes, we provide the configurable
circuit design and post-simulation scripts to easily program RRAM cells into the desired multilevel value.

# Requirements
* Cadence Spectre Circuit Simulator
* Python 3.5+
	* Pandas
	* Numpy
	* Plotly
	* Matplotlib
* Gnuplot 5.2+

# Project structure

Folders
```
resistive_controlled_scheme...[root]
  * cadence...............................[Spectre resources ]
    * results.............................[csv with transients and read resistances]
      * nominal_results...................[transients for level characterization]
      * mc_results........................[MC results]
          * mc_clip_range_r_read..........[Limited resistance range results]
          * mc_full_range_r_read..........[Full resistance range results]
    * netlists............................[Spectre scs]
        * characterization_simulations....[Simulations to characterize 1R and 1T1R RRAM cells]
        * montecarlo_simulations..........[MC Simulations]
        * nominal_simulations.............[Nominal Simulations to characterize levels]
        * ommit...........................[Auxiliar subcircuits: RRAM cells, resistive loads, muxes...]
    * python..............................[Python scripts ]
      * python_circuitry_generation.......[Scripts to automate RRAMs/muxes/loads generation]
      * python_post_mc_study..............[Scripts to automate MC results analysis]
      * python_post_nominal_study.........[Scripts to automate nominal/levels results analysis]
      * python_RRAM_model_study...........[Scripts to analyze the RRAM model]
  * LICENSE
  * README
```

# RRAM Model
RRAM Model from Arizona State University
Developers and contact information:
Pai-Yu Chen, Shimeng Yu, Arizona State University
For technical questions, address to Pai-Yu Chen, pchen72@asu.edu
For logistic questions, address to Prof. Shimeng Yu, shimengy@asu.edu

Extracted from manual:
Copyright of the model is maintained by the developers, and the model is distributed under the
terms of the Creative Commons Attribution-NonCommercial 4.0 International Public License
http://creativecommons.org/licenses/by-nc/4.0/legalcode. If you use this model in your work, you are
requested to cite [1] in the reference
[1] P.-Y. Chen, S. Yu, “Compact modeling of RRAM devices and its applications in 1T1R and 1S1R
array design,” IEEE Trans. Electron Devices, vol. 62, no. 12, pp. 4022-4028, 2015.

# CMOS Technology
A commertial 40nm technology was used.
Substitute it with the most convinient one, but take into account that
results may vary depending on it. You must rerun the whole methodology.

# From the paper submitted to IEEE

	Memristor crossbar arrays naturally accelerates
	neural networks applications by carrying out
	parallel multiply-add operations.
	Due to the abrupt SET operation characterizing most
	RRAM devices, on-chip training usually requires either from
	iterative write/read stages, huge and variations-sensitive circuitry, or both,
	in order to achieve multilevel capabilities.
	This paper presents a novel architecture to achieve
	multilevel capabilities with a short and fixed operation duration.
	We rely on an ad-hoc scheme to self-control the abrupt SET,
	choking the writing stimulus as the cell addresses the desired level.
	We validated the proposal against thorough simulations
	using RRAM cells fitting extremely fast physical devices
	and a commercial $40$$nm$ CMOS technology, both exhibiting variability.
	In every case the proposed architecture allowed progressive and almost-linear resistive
	levels in each 1T1R and 1R crossbars structures.
