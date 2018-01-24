# rram_multilevel_driver
Architecture for 2-step (non-iterative) RRAM multilevel programming

## Description
The present framework provides the circuit designer with the design
and software tools to ensure the reliable programming of MLC RRAMs.

This architecture/methodology aims to be used with MLC RRAM cells suffering from
abrupt SET operations that otherwise require from multiple iterations to accurately tune the cell into the desired resistive state.

Valid for both 1T1R and 1R schemes, we provide the configurable
circuit design and post-simulation scripts to easily program RRAM cells into the desired multilevel value.

## TODO
* Clean crossbar autogeneration script

# Requirements
* Cadence Spectre Circuit Simulator
* CMOS / RRAM PDK:
	* CMOS PDK to be studied. [Open source Example: FreePDKTM] (https://www.eda.ncsu.edu/wiki/FreePDK) 
	* RRAM PDK to be studied.
		* [Open source example: ASU RRAM PDK] (http://faculty.engineering.asu.edu/shimengyu/model-downloads/)
		* [Open source example: Aristotle University of Thessalonica / Southampton University RRAM Model] (https://eprints.soton.ac.uk/411693/) DOI; 10.1109/TCAD.2018.2791468
* Python 3.5+
  * Pandas
  * Numpy
  * Plotly
  * Matplotlib
* Gnuplot 5.2+

**Please, be aware that some scripts (aka those using gnuplot) require from specific folder structures**
Read Carefully the console output after running the scripts

# Netlist Simulation
Netlists have been designed to be simulated with Cadence Spectre.
Adecuarte the technology paths and then run the simulation with:

    spectre ++aps=conservative ++parasitics arizona_rram_1t1r.scs

# Project structure

**Please, be aware that some scripts (aka those using gnuplot) require from specific folder structures**
Read Carefully the console output after running the scripts

Folders
```
resistive_controlled_scheme...[root]
  * cadence.........................................................[Spectre resources ]
    * results.......................................................[csv with transients and read resistances]
      * rram_characterization_results...............................[transients for rram characterization]
      * driver_characterization_results.............................[transients for level characterization]
      * nominal_results.............................................[transients for nominal simulations]
      * mc_results..................................................[MC results]
          * only_intra_device_variability...........................[Only intra device variability considered]
              * full_range..........................................[Whole resistance range considered]
              * clip_range..........................................[Optimized resistance range considered]
          * inter_intra_device_variability..........................[device to device and intra device variability considered]
              * full_range..........................................[Whole resistance range considered]
              * clip_range..........................................[Optimized resistance range considered]
    * netlists......................................................[Spectre scs]
        * rram_characterization_simulations.........................[Netlists for rram characterization]
        * driver_characterization_simulations.......................[Netlists for level characterization]
        * nominal_simulations.......................................[Netlists for nominal simulations]
        * montecarlo_simulations_inter_intra_device_simulations.....[device to device and intra device variability considered]
        * montecarlo_simulations_intra_device_simulations...........[Only intra device variability considered]
        * ommit.....................................................[Auxiliar subcircuits: RRAM cells, resistive loads, muxes...]
    * python........................................................[Python scripts ]
      * python_circuitry_generation.................................[Scripts to automate RRAMs/muxes/loads generation]
      * python_post_mc_study........................................[Scripts to automate MC results analysis]
      * python_post_driver_characterization_study...................[Scripts to automate nominal/levels results analysis]
      * python_rram_model_study.....................................[Scripts to analyze the RRAM model]
  * LICENSE
  * README
```

# Technologies used in article submitted to IEEE TCAS1

Different CMOS/RRAM models can be used. See requirements section.
The following models were used for the results shown in IEEE TCAS1 submission. 

## RRAM Model
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

## CMOS Technology
A commercial 40nm technology was used.
Substitute it with the most convenient one, but take into account that
results may vary depending on it. You must rerun the whole methodology.

# Abstract from the paper submitted to IEEE TCAS1

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
