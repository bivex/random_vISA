/* ========================================================================= */
/* Sail Formal Specification for RVV_Custom_ISA (V-ISA)                         */
/* Version: 1.0-synth                                                   */
/* Generated via Hexagonal DDD random_vISA Synthesizer                       */
/* ========================================================================= */

default Order dec
$include <prelude.sail>

let VLEN : int = 128
let ELEN : int = 64
let NUM_VREGS : int = 32

type vreg_idx = range(0, 31)
type vreg_t = bits(VLEN)

register v0  : vreg_t
register v1  : vreg_t
register v2  : vreg_t
register v3  : vreg_t
register vl  : bits(64)
register vtype : bits(64)

val get_velem : (vreg_t, int, int) -> bits(32)
val set_velem : (vreg_t, int, int, bits(32)) -> unit
val get_vmask_bit : (vreg_t, int) -> bits(1)

/* Instruction: vadd_vi_0 (OPIVI) */
/* Randomized vector add operation (OPIVI) */
val execute_vadd_vi_0 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vadd_vi_0(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = simm5;
      let res_elem = (op2 + op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vand_vv_1 (OPIVV) */
/* Randomized vector and operation (OPIVV) */
val execute_vand_vv_1 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vand_vv_1(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = (op2 & op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vmax_vv_2 (OPIVV) */
/* Randomized vector max operation (OPIVV) */
val execute_vmax_vv_2 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vmax_vv_2(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = max(op2, op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vadd_vv_3 (OPIVV) */
/* Randomized vector add operation (OPIVV) */
val execute_vadd_vv_3 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vadd_vv_3(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = (op2 + op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vnot_m_4 (OPMVV) */
/* Randomized unary vector not operation */
val execute_vnot_m_4 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vnot_m_4(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = (~op2);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vsadd_vx_5 (OPIVX) */
/* Randomized vector sadd operation (OPIVX) */
val execute_vsadd_vx_5 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vsadd_vx_5(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = rs1_val;
      let res_elem = (op2 +_sat op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vctz_m_6 (OPMVV) */
/* Randomized unary vector ctz operation */
val execute_vctz_m_6 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vctz_m_6(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = ctz(op2);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vadd_vv_7 (OPIVV) */
/* Randomized vector add operation (OPIVV) */
val execute_vadd_vv_7 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vadd_vv_7(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = (op2 + op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}
