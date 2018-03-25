----------------------------------------------------------------------------------
-- Company:    LSI UPM
-- Engineer:   Fernando Garca Redondo.
-- Contact:    fgarcia@die.upm.es
-- License:    Ask fgarcia@die.upm.es
--
-- Create Date:  30/11/2017
-- Design Name:
-- Module Name:  control
-- Description:   Project constants and definitions
--
-- Dependencies:
--
-- Revision 0.1, 30/11/2017
--
-- Additional Comments:
----------------------------------------------------------------------------------


library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
-- Project library
library work;
use work.control_pkg.ALL;

entity control_manager is
  generic (
    c_CLK_FREQ              : positive  := c_SYSTEM_CLK_FREQ;
    c_SET_NS                : positive  := c_SYSTEM_SET_NS;
    c_RESET_NS              : positive  := c_SYSTEM_RESET_NS;
    c_MAX_COUNT             : positive  := c_SYSTEM_MAX_COUNT
   );
  port (
    rst_i         : in  std_logic;
    clk_i         : in  std_logic;
    start_op_i    : in  std_logic;
    v_en_reset_o  : out std_logic;
    v_en_set_o    : out std_logic
  );
end control_manager;

architecture Behavioral of control_manager is

  -- states
  type control_states is (st_IDLE, st_RESET, st_SET);
  signal st_state, st_next_state  : control_states        := st_IDLE;

  -- counter signals
  signal cnt_counter               : unsigned(c_MAX_COUNT-1 downto 0);
  signal cnt_en                    : std_logic;
  signal s_v_en_reset, s_v_en_set  : std_logic;

begin

  -- Outputs
  v_en_reset_o <= s_v_en_reset;
  v_en_set_o   <= s_v_en_set;

  -- Generate counter
  p_counter: process (clk_i, rst_i)
  begin
      if (rst_i = '1') then
            cnt_counter <= (others => '0');
      elsif (rising_edge (clk_i)) then
          if (st_state = st_IDLE) then
              cnt_counter <= (others => '0');
          elsif cnt_en = '1' then
              cnt_counter <= cnt_counter + 1;
          end if;
      end if;
  end process p_counter;

  -- Register states
  p_sync_FSM: process(clk_i, rst_i)
  begin
      if rst_i = '1' then
         st_state <= st_IDLE;
      elsif rising_edge(clk_i) then
          st_state <= st_next_state;
      end if;
  end process p_sync_FSM;


  -- Next state logic
  p_next_state: process(st_state, cnt_counter, start_op_i)
  begin
      st_next_state <= st_state;
      case(st_state) is
          -- If calibration is done successfully
          when st_IDLE =>
              if start_op_i = '1' then
                  st_next_state <= st_RESET;
              end if;
          when st_RESET =>
              if cnt_counter > c_RESET_NS-1 then
                  st_next_state <= st_SET;
              end if;
          when st_SET =>
              if cnt_counter > c_SET_NS-1 then
                  st_next_state <= st_IDLE;
              end if;
          when others => st_next_state <= st_IDLE;
      end case;
  end process;


  -- counter enable, including ack response
  p_counter_en: process (clk_i, rst_i)
  begin
      if (rst_i = '1') then
            cnt_en    <= '0';
      elsif (rising_edge (clk_i)) then
          if (st_state = st_RESET or st_state = st_SET) then
              cnt_en    <= '1';
          else
              cnt_en    <= '0';
          end if;
      end if;
  end process p_counter_en;

  -- Control signals
  p_control:process(st_state, cnt_counter)
  begin
      s_v_en_reset   <= '0';
      s_v_en_set     <= '0';
      case(st_state) is
          when st_IDLE =>
              s_v_en_reset   <= '0';
              s_v_en_set     <= '0';
          when st_RESET =>
              s_v_en_reset   <= '1';
              s_v_en_set     <= '0';
          when st_SET =>
              s_v_en_reset   <= '0';
              s_v_en_set     <= '1';
          when others =>
              s_v_en_reset   <= '0';
              s_v_en_set     <= '0';
      end case;
  end process p_control;

end Behavioral;
