// Q1_05: 入队数据采样
// source_type: rtl_derived_candidate_contract
// External specification review is pending.
module pilot_Q1_05_reference(
  input wire clock,
  input wire reset,
  input wire [7:0] io_deq_bits,
  input wire [7:0] io_enq_bits,
  input wire io_enq_ready,
  input wire io_enq_valid
);
  a_target: assert property (@(posedge clock) disable iff (reset)
    (io_enq_ready && io_enq_valid) |=> (io_deq_bits == $past(io_enq_bits)));
  c_trigger: cover property (@(posedge clock) disable iff (reset) (io_enq_ready && io_enq_valid));
endmodule
bind Queue1_UInt8 pilot_Q1_05_reference checker_Q1_05_reference (.clock(clock), .reset(reset), .io_deq_bits(io_deq_bits), .io_enq_bits(io_enq_bits), .io_enq_ready(io_enq_ready), .io_enq_valid(io_enq_valid));
