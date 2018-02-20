This folder gathers the results extracted from Spectre simulations

# Nominal Results
Exported using viva
  * if exported from viva:
      first row: headers
      (maybe inbetween rows)
      second/last row: data in X0 Y0, X1, Y1 format, grab all Y values

# MC Results
Exported using spectre oceanEval function
    data is in two columns
    (level, read_data)

# Example expressions:

    value(getData("rram_0.mem_0:rram_r_read" ?result "tran") 130n)

    value(getData("rram_0.mem_0:rram_r_read" ?result "tran" ?resultsDir "./arizona_rram_1t1r.raw") 130n)


    value(getData("rram_0.mem_0:rram_r_read" ?result "tran" ?resultsDir "./mc_g_0_clip_1r/montecarlo_simulations/arizona_rram_1r.raw") 130n)
    value(getData("rram_0.mem_0:rram_r_read" ?result "tran" ?resultsDir "./mc_g_0_clip_1t1r/montecarlo_simulations/arizona_rram_1t1r.raw") 130n)
    value(getData("rram_0.mem_0:rram_r_read" ?result "tran" ?resultsDir "./mc_g_1_clip_1r/montecarlo_simulations/arizona_rram_1r.raw") 130n)
    value(getData("rram_0.mem_0:rram_r_read" ?result "tran" ?resultsDir "./mc_g_1_clip_1t1r/montecarlo_simulations/arizona_rram_1t1r.raw") 130n)
