import cocotb
from cocotb.triggers import Timer, FallingEdge
from cocotb.regression import TestFactory

@cocotb.test()
async def test(dut):
    dut._log.info("Starting traffic_controller test")

    # Reset procedure
    dut.rst_n <= 0
    await Timer(1, units='ns')
    dut.rst_n <= 1
    await Timer(1, units='ns')

    # Defining the count values based on the MAX_COUNT (10 seconds)
    GREEN_DURATION_NS = 30e9  # 30 seconds in ns
    YELLOW_DURATION_NS = 3e9  # 3 seconds in ns
    RED_DURATION_NS = 10e9  # 10 seconds in ns

    # Define a helper function to check the light outputs
    async def check_lights(direction, red, green, yellow):
        """Check the lights for a given direction."""
        assert dut.uo_out[direction*2 + 1] == red
        assert dut.uo_out[direction*2 + 2] == green
        # Note: There is no individual light output for yellow, so it is derived from red and green being off
        if yellow:
            assert dut.uo_out[direction*2 + 1] == 0
            assert dut.uo_out[direction*2 + 2] == 0
        return

    # For each direction, ensure lights go through the correct sequence of GREEN -> YELLOW -> RED
    for direction in range(4):
        dut._log.info(f"Testing direction {direction}")

        # Set the request for the current direction
        dut.ui_in <= 1 << direction

        # Check for GREEN
        await Timer(GREEN_DURATION_NS, units='ns')
        await check_lights(direction, red=0, green=1, yellow=0)

        # Check for YELLOW
        await Timer(YELLOW_DURATION_NS, units='ns')
        await check_lights(direction, red=0, green=0, yellow=1)

        # Check for RED
        await Timer(RED_DURATION_NS - YELLOW_DURATION_NS, units='ns')  # Subtracting yellow time as we've already waited that much
        await check_lights(direction, red=1, green=0, yellow=0)

    dut._log.info("Completed traffic_controller test")

# Register the test.
factory = TestFactory(test)
factory.generate_tests()
