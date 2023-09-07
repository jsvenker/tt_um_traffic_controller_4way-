import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles
from cocotb.binary import BinaryValue

async def reset_dut(rst_n, clk):
    """Reset DUT."""
    rst_n <= 0
    for _ in range(2):
        await RisingEdge(clk)
    rst_n <= 1
    await RisingEdge(clk)

@cocotb.test()
async def test_traffic_controller_4way(dut):
    dut._log.info("Creating clock")
    clock = Clock(dut.clk, 1, units="us")
    cocotb.fork(clock.start())

    # Reset DUT
    await reset_dut(dut.rst_n, dut.clk)
    
    dut.ena <= 1  # Enable the traffic controller

    # Testing different input patterns for ui_in
    # These patterns will change the current_direction and simulate the flow through different lights.
    input_patterns = [0x01, 0x02, 0x04, 0x08]

    for pattern in input_patterns:
        dut.ui_in <= BinaryValue(pattern)
        await ClockCycles(dut.clk, 5)
        dut._log.info(f"ui_in={pattern}, uo_out={dut.uo_out.value}, uio_out={dut.uio_out.value}")

        # Additional test logic and assertions can be added here based on expected outputs.

    # Disable the traffic controller
    dut.ena <= 0
    await ClockCycles(dut.clk, 5)

    dut._log.info("Test complete")

