![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/test/badge.svg)

# What is Tiny Tapeout?

TinyTapeout is an educational project that aims to make it easier and cheaper than ever to get your digital designs manufactured on a real chip!

Go to https://tinytapeout.com for instructions!

## What is this project?
This project was started to assist in upreving educational efforts in semiconductor engineering at the University of Arkansas, by providing an accessible path to learn the RTL-GDS open source design flow, and to demonstrate modern digital ASIC design easily. 

You can feel free to contact me at jsvenker@uark.edu with any questions, suggestions, comments or opportunities for collaboration.

The idea behind this project was to migrate an undergraduate FPGA-based HDL lab with chatGPT and tinytapeout to quickly arrive at an ASIC implementation. As the design was 100% generated by GPT4 with the exception of this paragraph, the full validity of the design is highly questionable. 

## Image of GDS
[3D Viewer](https://gds-viewer.tinytapeout.com/?model=https://jsvenker.github.io/tt_um_traffic_controller_4way-/tinytapeout.gds.gltf)
<br>
Commands:
<br>
    1 Hides Filler
    <br>
    2 Hides Routing (external to standard cells)
    <br>
    3 Displays currently selected cell
    <br>

![alt text](https://camo.githubusercontent.com/b1827335b1c1d7af2dcc2cf95eecef3b55e8fc3982cd5316e1bb088c4de19229/68747470733a2f2f6a7376656e6b65722e6769746875622e696f2f74745f756d5f747261666669635f636f6e74726f6c6c65725f347761792d2f6764735f72656e6465722e706e67)


## Resources

- [FAQ](https://tinytapeout.com/faq/)
- [Digital design lessons](https://tinytapeout.com/digital_design/)
- [Learn how semiconductors work](https://tinytapeout.com/siliwiz/)
- [Join the community](https://discord.gg/rPK2nSjxy8)

## Description
The design is a Verilog-based module called tt_um_traffic_controller_4way. It represents a 4-way traffic controller that manages the state (Red, Green, Yellow) of traffic lights at an intersection. Each direction (north, south, east, west) is represented by a binary code and has individual red, green, and yellow lights.


## How the Design Works
The module uses a 24-bit counter to manage the state durations. Three states are defined, RED, GREEN, and YELLOW, with corresponding durations.
Bidirectional pins (uio_out) control the Yellow lights, while unidirectional output pins (uo_out) manage the Red and Green lights. The direction of traffic is indicated by the   
current_direction register.

A reset signal is used to set the system to its initial state. The controller then sequences through the traffic light states based on the current value of the counter and the direction of 
traffic.

The system accepts inputs (ui_in) to select the current direction (north, south, east, west), which dictates which set of traffic lights are active.

## How to Test
The Python cocotb testbench sets up a simulation for the traffic light controller. The simulation includes...
    Creating a clock with a period of 1us.
    Resetting the DUT (Device Under Test).
    Enabling the traffic controller.
    Iteratively applying different input patterns (0x01, 0x02, 0x04, 0x08) to ui_in to simulate selecting different directions. For each pattern, the test waits for 5 clock cycles and then logs 
    the outputs uo_out and uio_out.
    Disabling the traffic controller.
    The test completes after running all input patterns.

  
  ## Simple Test Using a Breadboard...

    Connect the Verilog module's outputs to LED indicators on a breadboard.
    uo_out[1] to uo_out[7] pins can be connected to 7 LEDs representing the RED and GREEN lights for four directions.
    uio_out[1], uio_out[3], uio_out[5], and uio_out[7] pins can be connected to 4 LEDs representing the YELLOW lights for each direction.
    Connect the clock input (clk) to a clock source, like an oscillator, running at a frequency of 1MHz.
    Connect the rst_n pin to a push-button for manual reset.

    Power on the design.
    Press the reset button.
    Use a set of switches to manually set values for ui_in (ranging from 0x01 to 0x08) to select different directions.
    Observe the LEDs turning ON/OFF, representing different states of the traffic lights for the chosen direction.
    Repeat the process for different ui_in values.

    If the LEDs light up according to the expected behavior of the traffic light states, the design works as intended in a real-life setting.
    
  ## I/O
  <br> 
  In:
  <br> 
    ui_in - 8-bit input that selects the current traffic direction. Each of the lower 4 bits represents a direction. Setting a bit to '1' activates the corresponding direction. For example...
    <br> 
    ui_in[0] - Direction 1
    <br> 
    ui_in[1] - Direction 2
    <br> 
    ui_in[2] - Direction 3
    <br> 
    ui_in[3] - Direction 4
    <br> 
    uio_in - 8-bit bidirectional input, currently unused in this design.
    <br> 
    ena - Enable signal. When set to '1', the traffic controller is active. When set to '0', the controller is inactive.
    <br> 
    clk - Clock signal. It regulates the operation of the state machine and other sequential elements in the design.
    <br> 
    rst_n - Reset signal. When set to '0', the design resets and initializes to the RED state with the default direction. When set to '1', the design operates normally.
    <br> 
  Out:
  <br> 
    uo_out - 8-bit output signal representing the RED and GREEN light states for each direction. The encoding is as follows...
    <br> 
    uo_out[0] - Reserved bit, always '0'
    <br> 
    uo_out[1] - RED light for Direction 1
    <br> 
    uo_out[2] - GREEN light for Direction 1
    <br> 
    uo_out[3] - RED light for Direction 2
    <br> 
    uo_out[4] - GREEN light for Direction 2
    <br> 
    uo_out[5] - RED light for Direction 3
    <br> 
    uo_out[6] - GREEN light for Direction 3
    <br> 
    uo_out[7] - RED light for Direction 4
    <br> 
  Bi-Dir:
  <br> 
    uio_out[0] - Reserved bit, always '0'
    <br> 
    uio_out[1] - YELLOW light for Direction 1
    <br> 
    uio_out[2] - Reserved bit, always '0'
    <br> 
    uio_out[3] - YELLOW light for Direction 2
    <br> 
    uio_out[4] - Reserved bit, always '0'
    <br> 
    uio_out[5] - YELLOW light for Direction 3
    <br> 
    uio_out[6] - Reserved bit, always '0'
    <br> 
    uio_out[7] - YELLOW light for Direction 4
    <br> 
    uio_oe - 8-bit output enable signal for the bidirectional pins. All bits are set to '1' to enable the uio_out pins.

