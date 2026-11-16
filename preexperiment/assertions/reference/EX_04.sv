// EX_04: 停用后清除工作状态
// source_type: rtl_derived_candidate_contract
// External specification review is pending.
module pilot_EX_04_reference(
  input wire clock,
  input wire reset,
  input wire io_deact,
  input wire working
);
  a_target: assert property (@(posedge clock) disable iff (reset)
    (io_deact) |=> (!working));
  c_trigger: cover property (@(posedge clock) disable iff (reset) (io_deact));
endmodule
bind ExclusiveMonitorEntry pilot_EX_04_reference checker_EX_04_reference (.clock(clock), .reset(reset), .io_deact(io_deact), .working(working));
