// ARB_01: 输出有效性
// source_type: rtl_derived_candidate_contract
// External specification review is pending.
module pilot_ARB_01_reference(
  input wire clock,
  input wire reset,
  input wire io_in_0_valid,
  input wire io_in_1_valid,
  input wire io_out_valid
);
  a_target: assert property (@(posedge clock) disable iff (reset)
    (1'b1) |-> (io_out_valid == (io_in_0_valid || io_in_1_valid)));
  c_trigger: cover property (@(posedge clock) disable iff (reset) (1'b1));
endmodule
bind XsRRArbiter pilot_ARB_01_reference checker_ARB_01_reference (.clock(clock), .reset(reset), .io_in_0_valid(io_in_0_valid), .io_in_1_valid(io_in_1_valid), .io_out_valid(io_out_valid));
