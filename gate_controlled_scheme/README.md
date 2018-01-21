# rram_multilevel_driver: Gate Controlled Writing Scheme

Gate Controlled Writing Scheme have been used to accurately achieve MLC capabilities in RRAM cells with abrupt SETs.


* J. Woo et al., “Optimized Programming Scheme Enabling Linear
Potentiation in Filamentary HfO 2 RRAM Synapse for Neuromorphic
Systems,” IEEE Trans. Electron Devices, vol. 63, no. 12, pp. 5064–5067,
dec 2016.
* E. J. Merced-Grafals et al., “Repeatable, accurate, and high speed multi-
level programming of memristor 1T1R arrays for power efficient analog
computing applications,” Nanotechnology, vol. 27, no. 36, p. 365202,
sep 2016.

However, these schemes may require multiple iterative pulses  to perform the operation,
but more importantly, rely on the in-series transistor connected to the RRAM device.
Therefore variability greatly affects the operation.

## Description
This examples show how variability makes impractical, with the current (40nm and bellow) CMOS technologies,
the accurately MLC capabilities across different devices present in the crossbar.

We make use of

# Requirements
* Cadence Spectre Circuit Simulator
* [Circuit Reliability Framework] (https://github.com/fgr1986/circuit_reliability_framework) Framework interacting with Spectre handling the whole of the reliability simulations.
* CMOS / RRAM PDK:
	* CMOS PDK to be studied. [Open source Example: FreePDKTM] (https://www.eda.ncsu.edu/wiki/FreePDK)
	* RRAM PDK to be studied.
		* [Open source example: ASU RRAM PDK] (http://faculty.engineering.asu.edu/shimengyu/model-downloads/)
		* [Open source example: Aristotle University of Thessalonica / Southampton University RRAM Model] (https://eprints.soton.ac.uk/411693/) DOI; 10.1109/TCAD.2018.2791468
* Gnuplot 5.2+
