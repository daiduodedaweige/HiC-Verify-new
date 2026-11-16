// ARB_05: 轮询状态仅在接受时更新
// source_type: rtl_derived_candidate_contract
// External specification review is pending.
module pilot_ARB_05_reference(
  input wire clock,
  input wire reset,
  input wire arb_ctrl_validMask_grantMask_lastGrant,
  input wire arb_io_chosen_choice,
  input wire io_out_ready,
  input wire io_out_valid
);
  a_target: assert property (@(posedge clock) disable iff (reset)
    (io_out_valid && io_out_ready) |=> (arb_ctrl_validMask_grantMask_lastGrant == $past(arb_io_chosen_choice)));
  c_trigger: cover property (@(posedge clock) disable iff (reset) (io_out_valid && io_out_ready));
endmodule
bind XsRRArbiter pilot_ARB_05_reference checker_ARB_05_reference (.clock(clock), .reset(reset), .arb_ctrl_validMask_grantMask_lastGrant(arb_ctrl_validMask_grantMask_lastGrant), .arb_io_chosen_choice(arb_io_chosen_choice), .io_out_ready(io_out_ready), .io_out_valid(io_out_valid));
