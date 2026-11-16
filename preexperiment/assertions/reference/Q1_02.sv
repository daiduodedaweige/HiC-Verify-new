// Q1_02: 阻塞时保持有效
// source_type: rtl_derived_candidate_contract
// External specification review is pending.
module pilot_Q1_02_reference(
  input wire clock,
  input wire reset,
  input wire io_deq_ready,
  input wire io_deq_valid
);
  a_target: assert property (@(posedge clock) disable iff (reset)
    (io_deq_valid && !io_deq_ready) |=> (io_deq_valid));
  c_trigger: cover property (@(posedge clock) disable iff (reset) (io_deq_valid && !io_deq_ready));
endmodule
bind Queue1_UInt8 pilot_Q1_02_reference checker_Q1_02_reference (.clock(clock), .reset(reset), .io_deq_ready(io_deq_ready), .io_deq_valid(io_deq_valid));
