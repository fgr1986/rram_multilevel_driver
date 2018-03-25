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

library work;

library ieee;
use ieee.std_logic_1164.ALL;
use ieee.numeric_std.ALL;

package control_pkg is

  ---------------------------
  -- Components number    --
  ---------------------------
  ----------------------------------
  -- Freqs and speed constants   --
  ----------------------------------
  constant c_SYSTEM_CLK_FREQ        : integer   := 1000000000; --200000000; --198182500
  constant c_SYSTEM_CLK_EN          : std_logic := '1';

  ---------------------------
  -- Setup times        --
  ---------------------------
  constant c_SYSTEM_SET_NS          : integer   := 100*(1000000000/c_SYSTEM_CLK_FREQ);
  constant c_SYSTEM_RESET_NS        : integer   := 200*(1000000000/c_SYSTEM_CLK_FREQ);

  constant c_SYSTEM_MAX_COUNT       : integer   := 8; --2^8 = 256 > 200

end control_pkg;
