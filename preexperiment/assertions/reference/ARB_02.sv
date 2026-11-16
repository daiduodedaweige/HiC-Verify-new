// ARB_02: 实际接受传输互斥
// source_type: rtl_derived_candidate_contract
// External specification review is pending.
module pilot_ARB_02_reference(
  input wire clock,
  input wire reset,
  input wire io_in_0_ready,
  input wire io_in_0_valid,
  input wire io_in_1_ready,
  input wire io_in_1_valid
);
  a_target: assert property (@(posedge clock) disable iff (reset)
    (1'b1) |-> (!(io_in_0_valid && io_in_0_ready && io_in_1_valid && io_in_1_ready)));
  c_trigger: cover property (@(posedge clock) disable iff (reset) (1'b1));
endmodule
bind XsRRArbiter pilot_ARB_02_reference checker_ARB_02_reference (.clock(clock), .reset(reset), .io_in_0_ready(io_in_0_ready), .io_in_0_valid(io_in_0_valid), .io_in_1_ready(io_in_1_ready), .io_in_1_valid(io_in_1_valid));
