// ENC_05: 位一选择需要排除更低位
// source_type: rtl_derived_candidate_contract
// External specification review is pending.
module pilot_ENC_05_reference(
  input wire [7:0] i_data,
  input wire [7:0] o_code
);
  always_comb begin
    a_target: assert (!(!i_data[0] && i_data[1]) || (o_code == 8'h02));
    c_trigger: cover (!i_data[0] && i_data[1]);
  end
endmodule
bind PriorityEncoderOneHotLow8 pilot_ENC_05_reference checker_ENC_05_reference (.i_data(i_data), .o_code(o_code));
