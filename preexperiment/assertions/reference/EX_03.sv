// EX_03: 无预留或标签不符时拒绝存储
// source_type: rtl_derived_candidate_contract
// External specification review is pending.
module pilot_EX_03_reference(
  input wire clock,
  input wire reset,
  input wire corrReq,
  input wire io_req_exok,
  input wire io_req_ld,
  input wire tagMatch,
  input wire working
);
  a_target: assert property (@(posedge clock) disable iff (reset)
    (corrReq && !io_req_ld && (!working || !tagMatch)) |-> (!io_req_exok));
  c_trigger: cover property (@(posedge clock) disable iff (reset) (corrReq && !io_req_ld && (!working || !tagMatch)));
endmodule
bind ExclusiveMonitorEntry pilot_EX_03_reference checker_EX_03_reference (.clock(clock), .reset(reset), .corrReq(corrReq), .io_req_exok(io_req_exok), .io_req_ld(io_req_ld), .tagMatch(tagMatch), .working(working));
