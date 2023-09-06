import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_traffic_controller(dut):
    dut._log.info("Starting tt_um_traffic_controller_4way test")
    
    # Parameters
    MAX_COUNT = int(dut.MAX_COUNT.value)
    GREEN_DURATION = 3 * MAX_COUNT
    YELLOW_DURATION = (MAX_COUNT * 3) // 10
    
    clock = Clock(dut.clk, 1, units="us")  # Assuming a 1MHz clock for simplicity
    cocotb.start_soon(clock.start())

    # Reset sequence
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 1)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 10)  # Delay for stabilization

    async def check_lights(direction, red, green, yellow):
        """Check the lights for a given direction."""
        assert dut.uo_out[direction*2 + 1] == red
        assert dut.uo_out[direction*2] == green
        assert dut.uio_out[direction*2 + 1] == yellow

    for direction in range(4):
        dut._log.info(f"Testing direction {direction}")

        # Set the request for the current direction
        dut.ui_in.value = 1 << direction

        # Check for GREEN
        await check_lights(direction, red=0, green=1, yellow=0)

        # Wait for GREEN_DURATION and then check for YELLOW
        await ClockCycles(dut.clk, GREEN_DURATION)
        await check_lights(direction, red=0, green=0, yellow=1)

        # Wait for YELLOW_DURATION, then check for RED
        await ClockCycles(dut.clk, YELLOW_DURATION)
        await check_lights(direction, red=1, green=0, yellow=0)

    # Reset sequence
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Completed tt_um_traffic_controller_4way test")
