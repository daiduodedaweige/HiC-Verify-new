// ARB_04: 输入一事务身份转发
// source_type: rtl_derived_candidate_contract
// External specification review is pending.
module pilot_ARB_04_reference(
  input wire clock,
  input wire reset,
  input wire [11:0] io_in_1_bits_TxnID,
  input wire io_in_1_ready,
  input wire io_in_1_valid,
  input wire [11:0] io_out_bits_TxnID,
  input wire io_out_valid
);
  a_target: assert property (@(posedge clock) disable iff (reset)
    (io_in_1_valid && io_in_1_ready) |-> (io_out_valid && io_out_bits_TxnID == io_in_1_bits_TxnID));
  c_trigger: cover property (@(posedge clock) disable iff (reset) (io_in_1_valid && io_in_1_ready));
endmodule
bind XsRRArbiter pilot_ARB_04_reference checker_ARB_04_reference (.clock(clock), .reset(reset), .io_in_1_bits_TxnID(io_in_1_bits_TxnID), .io_in_1_ready(io_in_1_ready), .io_in_1_valid(io_in_1_valid), .io_out_bits_TxnID(io_out_bits_TxnID), .io_out_valid(io_out_valid));
