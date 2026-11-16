// Q6_01: 非满时允许入队
// source_type: rtl_derived_candidate_contract
// External specification review is pending.
module pilot_Q6_01_reference(
  input wire clock,
  input wire reset,
  input wire full,
  input wire io_enq_ready
);
  a_target: assert property (@(posedge clock) disable iff (reset)
    (!full) |-> (io_enq_ready));
  c_trigger: cover property (@(posedge clock) disable iff (reset) (!full));
endmodule
bind Queue6_UInt2 pilot_Q6_01_reference checker_Q6_01_reference (.clock(clock), .reset(reset), .full(full), .io_enq_ready(io_enq_ready));
