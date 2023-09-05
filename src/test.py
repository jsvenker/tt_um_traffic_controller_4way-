import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, ClockCycles

@cocotb.test()
async def tt_um_traffic_controller_4way(dut):
    dut._log.info("Starting tt_um_traffic_controller_4way test")
    clock = Clock(dut.clk, 1, units="us")  # Using a 1MHz clock
    cocotb.start_soon(clock.start())

    # Reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # Defining the count values based on the MAX_COUNT (10 seconds)
    GREEN_DURATION_CYCLES = 30e6  # 30 seconds in clock cycles
    YELLOW_DURATION_CYCLES = 3e6  # 3 seconds in clock cycles
    RED_DURATION_CYCLES = 10e6 - GREEN_DURATION_CYCLES - YELLOW_DURATION_CYCLES  # Remaining time after subtracting green and yellow durations

    # Define a helper function to check the light outputs
    async def check_lights(direction, red, green):
        """Check the lights for a given direction."""
        print(f"uo_out: {dut.uo_out.value}, direction: {direction}, Expected Green: {green}")
        assert dut.uo_out[direction*2 + 1] == red
        assert dut.uo_out[direction*2 + 2] == green

    # For each direction, ensure lights go through the correct sequence of GREEN -> YELLOW -> RED
    for direction in range(4):
        dut._log.info(f"Testing direction {direction}")

        # Set the request for the current direction
        dut.ui_in.value = 1 << direction

        # Check for GREEN
        await ClockCycles(dut.clk, int(GREEN_DURATION_CYCLES))
        await check_lights(direction, red=0, green=1)

        # Check for YELLOW
        await ClockCycles(dut.clk, int(YELLOW_DURATION_CYCLES))
        await check_lights(direction, red=0, green=0)  # As per the design, yellow is indicated by both red and green being off

        # Check for RED
        await ClockCycles(dut.clk, int(RED_DURATION_CYCLES))
        await check_lights(direction, red=1, green=0)

     # Reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Completed tt_um_traffic_controller_4way test")
