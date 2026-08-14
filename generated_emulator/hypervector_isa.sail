/* ========================================================================= */
/* Sail Formal Specification for HyperVector_ISA (V-ISA)                         */
/* Version: 1.0-synth                                                   */
/* Generated via Hexagonal DDD random_vISA Synthesizer                       */
/* ========================================================================= */

default Order dec
$include <prelude.sail>

let VLEN : int = 256
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

/* Instruction: vand_vv_0 (OPIVV) */
/* Randomized vector and operation (OPIVV) */
val execute_vand_vv_0 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vand_vv_0(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = (op2 & op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vmax_vx_1 (OPIVX) */
/* Randomized vector max operation (OPIVX) */
val execute_vmax_vx_1 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vmax_vx_1(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let rs1_val = rX(vs1_or_imm);
      let op1 = rs1_val;
      let res_elem = max(op2, op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vdiv_vx_2 (OPIVX) */
/* Randomized vector div operation (OPIVX) */
val execute_vdiv_vx_2 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vdiv_vx_2(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let rs1_val = rX(vs1_or_imm);
      let op1 = rs1_val;
      let res_elem = (op2 / op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vxor_vx_3 (OPIVX) */
/* Randomized vector xor operation (OPIVX) */
val execute_vxor_vx_3 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vxor_vx_3(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let rs1_val = rX(vs1_or_imm);
      let op1 = rs1_val;
      let res_elem = (op2 ^ op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vdiv_vx_4 (OPIVX) */
/* Randomized vector div operation (OPIVX) */
val execute_vdiv_vx_4 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vdiv_vx_4(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let rs1_val = rX(vs1_or_imm);
      let op1 = rs1_val;
      let res_elem = (op2 / op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vmax_vv_5 (OPIVV) */
/* Randomized vector max operation (OPIVV) */
val execute_vmax_vv_5 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vmax_vv_5(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = max(op2, op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vdiv_vx_6 (OPIVX) */
/* Randomized vector div operation (OPIVX) */
val execute_vdiv_vx_6 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vdiv_vx_6(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let rs1_val = rX(vs1_or_imm);
      let op1 = rs1_val;
      let res_elem = (op2 / op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vor_vx_7 (OPIVX) */
/* Randomized vector or operation (OPIVX) */
val execute_vor_vx_7 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vor_vx_7(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let rs1_val = rX(vs1_or_imm);
      let op1 = rs1_val;
      let res_elem = (op2 | op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vsrl_vx_8 (OPIVX) */
/* Randomized vector srl operation (OPIVX) */
val execute_vsrl_vx_8 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vsrl_vx_8(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let rs1_val = rX(vs1_or_imm);
      let op1 = rs1_val;
      let res_elem = (op2 >> op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vclz_m_9 (OPMVV) */
/* Randomized unary vector clz operation */
val execute_vclz_m_9 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vclz_m_9(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = clz(op2);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vmin_vx_10 (OPIVX) */
/* Randomized vector min operation (OPIVX) */
val execute_vmin_vx_10 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vmin_vx_10(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let rs1_val = rX(vs1_or_imm);
      let op1 = rs1_val;
      let res_elem = min(op2, op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vmul_vv_11 (OPIVV) */
/* Randomized vector mul operation (OPIVV) */
val execute_vmul_vv_11 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vmul_vv_11(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = (op2 * op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vsrl_vv_12 (OPIVV) */
/* Randomized vector srl operation (OPIVV) */
val execute_vsrl_vv_12 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vsrl_vv_12(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = (op2 >> op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vsadd_vx_13 (OPIVX) */
/* Randomized vector sadd operation (OPIVX) */
val execute_vsadd_vx_13 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vsadd_vx_13(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let rs1_val = rX(vs1_or_imm);
      let op1 = rs1_val;
      let res_elem = (op2 +_sat op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vmul_vv_14 (OPIVV) */
/* Randomized vector mul operation (OPIVV) */
val execute_vmul_vv_14 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vmul_vv_14(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = (op2 * op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vmax_vx_15 (OPIVX) */
/* Randomized vector max operation (OPIVX) */
val execute_vmax_vx_15 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vmax_vx_15(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let rs1_val = rX(vs1_or_imm);
      let op1 = rs1_val;
      let res_elem = max(op2, op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}
