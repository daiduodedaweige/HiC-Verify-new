// Q6_04: 入队指针末项回绕
// source_type: rtl_derived_candidate_contract
// External specification review is pending.
module pilot_Q6_04_reference(
  input wire clock,
  input wire reset,
  input wire do_enq,
  input wire [2:0] enq_ptr_value
);
  a_target: assert property (@(posedge clock) disable iff (reset)
    (do_enq && enq_ptr_value == 3'd5) |=> (enq_ptr_value == 3'd0));
  c_trigger: cover property (@(posedge clock) disable iff (reset) (do_enq && enq_ptr_value == 3'd5));
endmodule
bind Queue6_UInt2 pilot_Q6_04_reference checker_Q6_04_reference (.clock(clock), .reset(reset), .do_enq(do_enq), .enq_ptr_value(enq_ptr_value));
