// Q6_03: 已存储队首阻塞保持
// source_type: rtl_derived_candidate_contract
// External specification review is pending.
module pilot_Q6_03_reference(
  input wire clock,
  input wire reset,
  input wire [2:0] deq_ptr_value,
  input wire empty,
  input wire [2:0] enq_ptr_value,
  input wire [1:0] io_deq_bits,
  input wire io_deq_ready,
  input wire io_deq_valid
);
  a_target: assert property (@(posedge clock) disable iff (reset)
    (!empty && !io_deq_ready) |=> (io_deq_valid && $stable(io_deq_bits)));
  c_trigger: cover property (@(posedge clock) disable iff (reset) (!empty && !io_deq_ready));
  a_queue_pointer_ranges: assert property (@(posedge clock) disable iff (reset)
    (enq_ptr_value < 3'd6 && deq_ptr_value < 3'd6));
endmodule
bind Queue6_UInt2 pilot_Q6_03_reference checker_Q6_03_reference (.clock(clock), .reset(reset), .deq_ptr_value(deq_ptr_value), .empty(empty), .enq_ptr_value(enq_ptr_value), .io_deq_bits(io_deq_bits), .io_deq_ready(io_deq_ready), .io_deq_valid(io_deq_valid));
