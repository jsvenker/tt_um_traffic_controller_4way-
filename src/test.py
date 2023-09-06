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
    await ClockCycles(dut.clk, 1)
    dut.rst_n.value = 1

    # Let's add a delay here to allow the traffic controller to stabilize after reset
    await ClockCycles(dut.clk, 10)

    # Log the initial state of uo_out
    dut._log.info(f"Initial uo_out: {dut.uo_out.value}")

    # Define a helper function to check the light outputs
    async def check_lights(direction, red, green):
        """Check the lights for a given direction."""
        dut._log.info(f"uo_out: {dut.uo_out.value}, direction: {direction}, Expected Green: {green}")
        assert dut.uo_out[direction*2 + 1] == red
        assert dut.uo_out[direction*2] == green

    # For each direction, ensure lights go through the correct sequence of GREEN -> YELLOW -> RED
    for direction in range(4):
        dut._log.info(f"Testing direction {direction}")

        # Set the request for the current direction
        dut.ui_in.value = 1 << direction

        # Wait for a few cycles to ensure the light is stable
        await ClockCycles(dut.clk, 5)

        # Check for GREEN
        await check_lights(direction, red=0, green=1)

        # Wait for a few cycles before transitioning to YELLOW
        await ClockCycles(dut.clk, 5)

        # Check for YELLOW (both red and green are off as per design)
        await check_lights(direction, red=0, green=0)

        # Wait for a few cycles before transitioning to RED
        await ClockCycles(dut.clk, 5)

        # Check for RED
        await check_lights(direction, red=1, green=0)

     # Reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Completed tt_um_traffic_controller_4way test")
