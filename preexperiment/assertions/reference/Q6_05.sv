// Q6_05: 两个指针均在合法范围
// source_type: rtl_derived_candidate_contract
// External specification review is pending.
module pilot_Q6_05_reference(
  input wire clock,
  input wire reset,
  input wire [2:0] deq_ptr_value,
  input wire [2:0] enq_ptr_value
);
  a_target: assert property (@(posedge clock) disable iff (reset)
    (1'b1) |-> (enq_ptr_value < 3'd6 && deq_ptr_value < 3'd6));
  c_trigger: cover property (@(posedge clock) disable iff (reset) (1'b1));
endmodule
bind Queue6_UInt2 pilot_Q6_05_reference checker_Q6_05_reference (.clock(clock), .reset(reset), .deq_ptr_value(deq_ptr_value), .enq_ptr_value(enq_ptr_value));
