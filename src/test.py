import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

# Define the expected states: RED, GREEN, YELLOW
states = {
    'RED': 0b001,
    'GREEN': 0b010,
    'YELLOW': 0b100
}

@cocotb.test()
async def test_traffic_controller_4way(dut):
    dut._log.info("Starting the test...")

    # Start the clock
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset the module
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 1)
    dut.rst_n.value = 1

    # Ensure it starts with RED state
    assert dut.uo_out[1] == states['RED']
    await ClockCycles(dut.clk, 1)

    # Stimulate request
    dut.ui_in.value = 0b0001

    # Check transitions over time
    # Assuming the counter changes states after MAX_COUNT cycles
    # We'll check the state after the cycle count to verify transitions

    await ClockCycles(dut.clk, dut.MAX_COUNT)
    assert dut.uo_out[2] == states['GREEN'], f"Expected GREEN but got {dut.uo_out[2]}"

    await ClockCycles(dut.clk, dut.MAX_COUNT)
    assert dut.uo_out[2] == states['YELLOW'], f"Expected YELLOW but got {dut.uo_out[2]}"

    await ClockCycles(dut.clk, dut.MAX_COUNT)
    assert dut.uo_out[1] == states['RED'], f"Expected RED but got {dut.uo_out[1]}"

    dut._log.info("Test completed!")
