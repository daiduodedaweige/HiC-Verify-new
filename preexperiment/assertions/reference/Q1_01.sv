// Q1_01: 流水入队就绪关系
// source_type: rtl_derived_candidate_contract
// External specification review is pending.
module pilot_Q1_01_reference(
  input wire clock,
  input wire reset,
  input wire io_deq_ready,
  input wire io_deq_valid,
  input wire io_enq_ready
);
  a_target: assert property (@(posedge clock) disable iff (reset)
    (1'b1) |-> (io_enq_ready == (io_deq_ready || !io_deq_valid)));
  c_trigger: cover property (@(posedge clock) disable iff (reset) (1'b1));
endmodule
bind Queue1_UInt8 pilot_Q1_01_reference checker_Q1_01_reference (.clock(clock), .reset(reset), .io_deq_ready(io_deq_ready), .io_deq_valid(io_deq_valid), .io_enq_ready(io_enq_ready));
