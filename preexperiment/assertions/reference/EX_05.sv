// EX_05: 对应请求记录地址标签
// source_type: rtl_derived_candidate_contract
// External specification review is pending.
module pilot_EX_05_reference(
  input wire clock,
  input wire reset,
  input wire corrReq,
  input wire [7:0] io_req_tag_adr,
  input wire [7:0] tag_adr
);
  a_target: assert property (@(posedge clock) disable iff (reset)
    (corrReq) |=> (tag_adr == $past(io_req_tag_adr)));
  c_trigger: cover property (@(posedge clock) disable iff (reset) (corrReq));
endmodule
bind ExclusiveMonitorEntry pilot_EX_05_reference checker_EX_05_reference (.clock(clock), .reset(reset), .corrReq(corrReq), .io_req_tag_adr(io_req_tag_adr), .tag_adr(tag_adr));
