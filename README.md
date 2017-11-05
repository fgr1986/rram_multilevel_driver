# rram_multilevel_driver
Architecture for RRAM multilevel programming

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
      * python_circuitry_generation.......[Scripts to automate muxes/loads generation]
      * python_post_mc_study..............[Scripts to automate MC results analysis]
      * python_post_nominal_study.........[Scripts to automate nominal/levels results analysis]
      * python_pre_study..................[Scripts to analyze the RRAM model]
  * LICENSE
  * README
```

# RRAM Model
RRAM Model from Arizona State University
Developers and contact information:
Pai-Yu Chen, Shimeng Yu, Arizona State University
For technical questions, address to Pai-Yu Chen, pchen72@asu.edu
For logistic questions, address to Prof. Shimeng Yu, shimengy@asu.edu
//
Extracted from manual:
//
Copyright of the model is maintained by the developers, and the model is distributed under the
terms of the Creative Commons Attribution-NonCommercial 4.0 International Public License
http://creativecommons.org/licenses/by-nc/4.0/legalcode. If you use this model in your work, you are
requested to cite [1] in the reference
[1] P.-Y. Chen, S. Yu, “Compact modeling of RRAM devices and its applications in 1T1R and 1S1R
array design,” IEEE Trans. Electron Devices, vol. 62, no. 12, pp. 4022-4028, 2015.
