#!/bin/bash

# Towards LRS
CONF_DIR=/simulation_data/circuit_reliability_framework/variability_simulator/experiments/tvlsi_2017_multilevel/conf_files
CADENCE_CONF=$CONF_DIR/xml/cadence_conf/cadence_conf.xml
# dummy
# TECHNOLOGY_CONF=$CONF_DIR/xml/technology_conf/technology_tsmc_40nm_18_conf_top_globalmc_localmc_with_driver.xml
TECHNOLOGY_CONF=$CONF_DIR/xml/technology_conf/technology_tsmc_40nm_18_conf_top_tt.xml
EXPERIMENT_CONF=$CONF_DIR/xml/tvlsi_2017_multilevel_conf/tvlsi_2017_multilevel_variability.xml
CIRCUIT_NETLIST=$CONF_DIR/netlists/tvlsi_2017_multilevel_set.scs
TITLE=tvlsi_2017_multilevel_variability_$RELIABILITY_FRAMEWORK_VERSION
PERMISSIVE_MODE=permissive
PROGRAM_BIN=/simulation_data/circuit_reliability_framework/variability_simulator/bin/variability_simulator_$RELIABILITY_FRAMEWORK_VERSION
# ND...
echo -en "c\n1\na\na\n" | $PROGRAM_BIN $CADENCE_CONF $TECHNOLOGY_CONF $EXPERIMENT_CONF $CIRCUIT_NETLIST $TITLE $PERMISSIVE_MODE;
mv rs_log.log log_tvlsi_2017_multilevel_top_tt_log.log
mv rs_error.log log_tvlsi_2017_multilevel_top_tt_error.log
