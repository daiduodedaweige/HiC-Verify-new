// Q1_03: 阻塞时保持数据
// source_type: rtl_derived_candidate_contract
// External specification review is pending.
module pilot_Q1_03_reference(
  input wire clock,
  input wire reset,
  input wire [7:0] io_deq_bits,
  input wire io_deq_ready,
  input wire io_deq_valid
);
  a_target: assert property (@(posedge clock) disable iff (reset)
    (io_deq_valid && !io_deq_ready) |=> ($stable(io_deq_bits)));
  c_trigger: cover property (@(posedge clock) disable iff (reset) (io_deq_valid && !io_deq_ready));
endmodule
bind Queue1_UInt8 pilot_Q1_03_reference checker_Q1_03_reference (.clock(clock), .reset(reset), .io_deq_bits(io_deq_bits), .io_deq_ready(io_deq_ready), .io_deq_valid(io_deq_valid));
