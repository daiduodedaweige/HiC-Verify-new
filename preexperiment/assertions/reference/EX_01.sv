// EX_01: 非对应请求不能成功
// source_type: rtl_derived_candidate_contract
// External specification review is pending.
module pilot_EX_01_reference(
  input wire clock,
  input wire reset,
  input wire corrReq,
  input wire io_req_exok
);
  a_target: assert property (@(posedge clock) disable iff (reset)
    (!corrReq) |-> (!io_req_exok));
  c_trigger: cover property (@(posedge clock) disable iff (reset) (!corrReq));
endmodule
bind ExclusiveMonitorEntry pilot_EX_01_reference checker_EX_01_reference (.clock(clock), .reset(reset), .corrReq(corrReq), .io_req_exok(io_req_exok));
