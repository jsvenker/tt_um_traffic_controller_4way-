import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, ClockCycles

@cocotb.test()
async def test_traffic_controller(dut):
    dut._log.info("Starting tt_um_traffic_controller_4way test")
    clock = Clock(dut.clk, 1, units="us")  # Using a 1MHz clock
    cocotb.start_soon(clock.start())

    # Reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # Since we're not able to retrieve MAX_COUNT from the DUT, let's use the hardcoded value
    MAX_COUNT = 10_000_000
    
    # Defining the count values based on the hardcoded MAX_COUNT (10 seconds)
    GREEN_DURATION_CYCLES = 30 * MAX_COUNT  # 30 seconds in clock cycles
    YELLOW_DURATION_CYCLES = (3 * MAX_COUNT) / 10  # 3 seconds in clock cycles
    RED_DURATION_CYCLES = MAX_COUNT - GREEN_DURATION_CYCLES - YELLOW_DURATION_CYCLES  # Remaining time

    # Define a helper function to check the light outputs
    async def check_lights(direction, red, green):
        """Check the lights for a given direction."""
        dut._log.info(f"uo_out: {dut.uo_out.value}, direction: {direction}, Expected Green: {green}")
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
