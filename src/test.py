import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, ClockCycles

@cocotb.test()
async def test_traffic_controller(dut):
    dut._log.info("Starting tt_um_traffic_controller_4way test")
    clock = Clock(dut.clk, 1, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    async def check_lights(direction, red, green):
        """Check the lights for a given direction."""
        assert dut.uo_out[direction*2 + 1] == red
        assert dut.uo_out[direction*2 + 2] == green

    TOTAL_CYCLE_DURATION = int(GREEN_DURATION_CYCLES + YELLOW_DURATION_CYCLES + RED_DURATION_CYCLES)

    for direction in range(4):
        dut._log.info(f"Testing direction {direction}")

        # Set the request for the current direction
        dut.ui_in.value = 1 << direction

        # Check for GREEN
        await ClockCycles(dut.clk, int(GREEN_DURATION_CYCLES))
        await check_lights(direction, red=0, green=1)

        # Check for YELLOW
        await ClockCycles(dut.clk, int(YELLOW_DURATION_CYCLES))
        await check_lights(direction, red=1, green=0)

        # Check for RED
        await ClockCycles(dut.clk, int(RED_DURATION_CYCLES))
        await check_lights(direction, red=1, green=0)

    # Give some additional cycles for the entire sequence to finish
    await ClockCycles(dut.clk, TOTAL_CYCLE_DURATION)

    # Reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Completed tt_um_traffic_controller_4way test")

