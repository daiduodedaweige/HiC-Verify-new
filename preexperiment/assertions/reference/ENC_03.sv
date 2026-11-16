// ENC_03: 输出只能选择有效输入位
// source_type: rtl_derived_candidate_contract
// External specification review is pending.
module pilot_ENC_03_reference(
  input wire [7:0] i_data,
  input wire [7:0] o_code
);
  always_comb begin
    a_target: assert (!(1'b1) || ((o_code & ~i_data) == 8'h00));
    c_trigger: cover (1'b1);
  end
endmodule
bind PriorityEncoderOneHotLow8 pilot_ENC_03_reference checker_ENC_03_reference (.i_data(i_data), .o_code(o_code));
