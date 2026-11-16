// ENC_01: 零输入产生零编码
// source_type: rtl_derived_candidate_contract
// External specification review is pending.
module pilot_ENC_01_reference(
  input wire [7:0] i_data,
  input wire [7:0] o_code
);
  always_comb begin
    a_target: assert (!(i_data == 8'h00) || (o_code == 8'h00));
    c_trigger: cover (i_data == 8'h00);
  end
endmodule
bind PriorityEncoderOneHotLow8 pilot_ENC_01_reference checker_ENC_01_reference (.i_data(i_data), .o_code(o_code));
