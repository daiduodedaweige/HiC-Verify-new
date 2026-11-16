// ARB_03: 输入零有效载荷转发
// source_type: rtl_derived_candidate_contract
// External specification review is pending.
module pilot_ARB_03_reference(
  input wire clock,
  input wire reset,
  input wire [107:0] io_in_0_bits_Payload,
  input wire io_in_0_ready,
  input wire io_in_0_valid,
  input wire [107:0] io_out_bits_Payload,
  input wire io_out_valid
);
  a_target: assert property (@(posedge clock) disable iff (reset)
    (io_in_0_valid && io_in_0_ready) |-> (io_out_valid && io_out_bits_Payload == io_in_0_bits_Payload));
  c_trigger: cover property (@(posedge clock) disable iff (reset) (io_in_0_valid && io_in_0_ready));
endmodule
bind XsRRArbiter pilot_ARB_03_reference checker_ARB_03_reference (.clock(clock), .reset(reset), .io_in_0_bits_Payload(io_in_0_bits_Payload), .io_in_0_ready(io_in_0_ready), .io_in_0_valid(io_in_0_valid), .io_out_bits_Payload(io_out_bits_Payload), .io_out_valid(io_out_valid));
