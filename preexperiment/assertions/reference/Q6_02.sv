// Q6_02: 空队列组合直通
// source_type: rtl_derived_candidate_contract
// External specification review is pending.
module pilot_Q6_02_reference(
  input wire clock,
  input wire reset,
  input wire empty,
  input wire [1:0] io_deq_bits,
  input wire io_deq_valid,
  input wire [1:0] io_enq_bits,
  input wire io_enq_valid
);
  a_target: assert property (@(posedge clock) disable iff (reset)
    (empty && io_enq_valid) |-> (io_deq_valid && io_deq_bits == io_enq_bits));
  c_trigger: cover property (@(posedge clock) disable iff (reset) (empty && io_enq_valid));
endmodule
bind Queue6_UInt2 pilot_Q6_02_reference checker_Q6_02_reference (.clock(clock), .reset(reset), .empty(empty), .io_deq_bits(io_deq_bits), .io_deq_valid(io_deq_valid), .io_enq_bits(io_enq_bits), .io_enq_valid(io_enq_valid));
