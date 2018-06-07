--*****************************************************************************
-- Simple testbench
--
--*****************************************************************************
library ieee;
use ieee.std_logic_1164.ALL;
use ieee.numeric_std.ALL;
use ieee.math_real.all;

-- use std.textio.all;

-- Project library
library work;
use work.control_pkg.ALL;

entity tb_control is
--  generic (
--    log_file:       string  := "tb_fir_blocks_my_out.log"
--  );
end tb_control;

architecture behavior of tb_control is


  constant clk_period           : time := 1 ns;
  constant nrst_pulse           : time := 2 us;
  --Inputs
  signal rst                    : std_logic := '0';
  signal clk                    : std_logic := '0';
  signal start_op               : std_logic := '0';

  --outputs
  signal v_en_reset    : std_logic;
  signal v_en_set     : std_logic;

begin

  cmp_control : entity work.control_manager
    port map (
      rst_i              => rst,
      clk_i              => clk,
      start_op_i         => start_op,
      v_en_reset_o       => v_en_reset,
      v_en_set_o         => v_en_set );

  clk_process : process
  begin
    clk <= '1';
    wait for clk_period/2;
      clk <= '0';
    wait for clk_period/2;
  end process clk_process;  

  rst_process : process
  begin
    rst <= '1';
    wait for nrst_pulse;
    rst <= '0';
    wait for 10*nrst_pulse;
    rst <= '1';
    wait for nrst_pulse;
    rst <= '0';
    wait for 10*nrst_pulse;
    rst <= '1';
    wait for nrst_pulse;
    rst <= '0';
    wait;
  end process;
  
  -- start_op
  start_op_process: process
  begin
    start_op <= '0';
    wait for 10*nrst_pulse;
    start_op <= '1';
    wait for 2*clk_period;
    start_op <= '0';
    wait;
  end process start_op_process;  
     
end behavior;
