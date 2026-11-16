// ENC_02: 最低位具有最高优先级
// source_type: rtl_derived_candidate_contract
// External specification review is pending.
module pilot_ENC_02_reference(
  input wire [7:0] i_data,
  input wire [7:0] o_code
);
  always_comb begin
    a_target: assert (!(i_data[0]) || (o_code == 8'h01));
    c_trigger: cover (i_data[0]);
  end
endmodule
bind PriorityEncoderOneHotLow8 pilot_ENC_02_reference checker_ENC_02_reference (.i_data(i_data), .o_code(o_code));
