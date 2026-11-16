// ENC_04: 输出允许零或独热
// source_type: rtl_derived_candidate_contract
// External specification review is pending.
module pilot_ENC_04_reference(
  input wire [7:0] o_code
);
  always_comb begin
    a_target: assert (!(1'b1) || ($onehot0(o_code)));
    c_trigger: cover (1'b1);
  end
endmodule
bind PriorityEncoderOneHotLow8 pilot_ENC_04_reference checker_ENC_04_reference (.o_code(o_code));
