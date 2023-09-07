import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer, ClockCycles
from cocotb.binary import BinaryValue

async def reset_dut(rst_n, clk):
    """Reset DUT."""
    rst_n.value = 0
    for _ in range(2):
        await RisingEdge(clk)
    rst_n.value = 1
    await RisingEdge(clk)

@cocotb.test()
async def test_traffic_controller_4way(dut):
    dut._log.info("Creating clock")
    clock = Clock(dut.clk, 1, units="us")
    cocotb.start_soon(clock.start())

    # Reset DUT
    await reset_dut(dut.rst_n, dut.clk)
    
    dut.ena.value = 1  # Enable the traffic controller

    # Testing different input patterns for ui_in
    input_patterns = [0x01, 0x02, 0x04, 0x08]

    for pattern in input_patterns:
        dut.ui_in.value = BinaryValue(pattern, n_bits=8)  # Ensure 8-bit assignment
        await ClockCycles(dut.clk, 5)
        dut._log.info(f"ui_in={pattern:08b}, uo_out={dut.uo_out.value}, uio_out={dut.uio_out.value}")

    # Disable the traffic controller
    dut.ena.value = 0
    await ClockCycles(dut.clk, 5)

    dut._log.info("Test complete")
