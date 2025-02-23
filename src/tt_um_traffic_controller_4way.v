`default_nettype none

module tt_um_traffic_controller_4way #( parameter MAX_COUNT = 24'd10_000_000 ) (
    input  wire [7:0] ui_in,    
    output wire [7:0] uo_out,   
    input  wire [7:0] uio_in,   
    output wire [7:0] uio_out,  
    output wire [7:0] uio_oe,   
    input  wire       ena,      
    input  wire       clk,      
    input  wire       rst_n     
);

    wire reset = !rst_n;
    reg [1:0] current_direction;
    reg [2:0] state;  // 3 states: RED, GREEN, YELLOW

    parameter RED = 3'b001,
              GREEN = 3'b010,
              YELLOW = 3'b100;

    reg [23:0] counter = 0;

    // State durations
    parameter GREEN_DURATION = 3 * MAX_COUNT;        
    parameter YELLOW_DURATION = (MAX_COUNT * 3) / 10;

    // Assign the bidirectional pins
    assign uio_oe = 8'b11111111;

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            state <= RED;
            current_direction <= 2'b00;
            counter <= 0;
        end else begin

            if (ui_in[3:0] != 0) begin
                if (ui_in[0]) current_direction <= 2'b00;
                else if (ui_in[1]) current_direction <= 2'b01;
                else if (ui_in[2]) current_direction <= 2'b10;
                else if (ui_in[3]) current_direction <= 2'b11;
                state <= GREEN;
                counter <= 0;
            end else if (state == GREEN && counter < GREEN_DURATION) begin
                counter <= counter + 1;
            end else if (state == YELLOW && counter < YELLOW_DURATION) begin
                counter <= counter + 1;
            end else if (state == RED && counter < MAX_COUNT) begin
                counter <= counter + 1;
            end else begin
                counter <= 0;
                if (state == GREEN) state <= YELLOW;
                else if (state == YELLOW) state <= RED;
                else if (state == RED) state <= GREEN;
            end
        end
    end

    // Assign output status to the respective traffic lights
    assign uo_out[0] = 1'b0;  // Reserved bit
    assign uo_out[1] = (current_direction == 2'b00) ? state[0] : 1'b0; // Red Light 1
    assign uo_out[2] = (current_direction == 2'b00) ? state[1] : 1'b0; // Green Light 1
    assign uo_out[3] = (current_direction == 2'b01) ? state[0] : 1'b0; // Red Light 2
    assign uo_out[4] = (current_direction == 2'b01) ? state[1] : 1'b0; // Green Light 2
    assign uo_out[5] = (current_direction == 2'b10) ? state[0] : 1'b0; // Red Light 3
    assign uo_out[6] = (current_direction == 2'b10) ? state[1] : 1'b0; // Green Light 3
    assign uo_out[7] = (current_direction == 2'b11) ? state[0] : 1'b0; // Red Light 4

    // Yellow lights through bidirectional pins
    assign uio_out[0] = 1'b0;
    assign uio_out[1] = (current_direction == 2'b00) ? state[2] : 1'b0; // Yellow Light 1
    assign uio_out[2] = 1'b0;
    assign uio_out[3] = (current_direction == 2'b01) ? state[2] : 1'b0; // Yellow Light 2
    assign uio_out[4] = 1'b0;
    assign uio_out[5] = (current_direction == 2'b10) ? state[2] : 1'b0; // Yellow Light 3
    assign uio_out[6] = 1'b0;
    assign uio_out[7] = (current_direction == 2'b11) ? state[2] : 1'b0; // Yellow Light 4

endmodule
