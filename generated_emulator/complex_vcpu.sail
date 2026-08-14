/* ========================================================================= */
/* Sail Formal Specification for complex_vcpu (V-ISA)                         */
/* Version: 1.0-synth                                                   */
/* Generated via Hexagonal DDD random_vISA Synthesizer                       */
/* ========================================================================= */

default Order dec
$include <prelude.sail>

let VLEN : int = 512
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

/* Instruction: vclz_m_0 (OPMVV) */
/* Randomized unary vector clz operation */
val execute_vclz_m_0 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vclz_m_0(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = clz(op2);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vor_vi_1 (OPIVI) */
/* Randomized vector or operation (OPIVI) */
val execute_vor_vi_1 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vor_vi_1(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let simm5 = sign_extend(vs1_or_imm);
      let op1 = simm5;
      let res_elem = (op2 | op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vxor_vx_2 (OPIVX) */
/* Randomized vector xor operation (OPIVX) */
val execute_vxor_vx_2 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vxor_vx_2(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
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

/* Instruction: vmin_vx_3 (OPIVX) */
/* Randomized vector min operation (OPIVX) */
val execute_vmin_vx_3 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vmin_vx_3(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
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

/* Instruction: vsadd_vx_4 (OPIVX) */
/* Randomized vector sadd operation (OPIVX) */
val execute_vsadd_vx_4 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vsadd_vx_4(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
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

/* Instruction: vsra_vx_5 (OPIVX) */
/* Randomized vector sra operation (OPIVX) */
val execute_vsra_vx_5 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vsra_vx_5(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let rs1_val = rX(vs1_or_imm);
      let op1 = rs1_val;
      let res_elem = (op2 >>_s op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vrem_vx_6 (OPIVX) */
/* Randomized vector rem operation (OPIVX) */
val execute_vrem_vx_6 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vrem_vx_6(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let rs1_val = rX(vs1_or_imm);
      let op1 = rs1_val;
      let res_elem = (op2 % op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vabs_m_7 (OPMVV) */
/* Randomized unary vector abs operation */
val execute_vabs_m_7 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vabs_m_7(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = abs(op2);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vclz_m_8 (OPMVV) */
/* Randomized unary vector clz operation */
val execute_vclz_m_8 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vclz_m_8(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = clz(op2);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vsrl_vx_9 (OPIVX) */
/* Randomized vector srl operation (OPIVX) */
val execute_vsrl_vx_9 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vsrl_vx_9(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
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

/* Instruction: vcpop_m_10 (OPMVV) */
/* Randomized unary vector cpop operation */
val execute_vcpop_m_10 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vcpop_m_10(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = cpop(op2);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vcpop_m_11 (OPMVV) */
/* Randomized unary vector cpop operation */
val execute_vcpop_m_11 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vcpop_m_11(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = cpop(op2);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vrem_vv_12 (OPIVV) */
/* Randomized vector rem operation (OPIVV) */
val execute_vrem_vv_12 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vrem_vv_12(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = (op2 % op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vxor_vx_13 (OPIVX) */
/* Randomized vector xor operation (OPIVX) */
val execute_vxor_vx_13 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vxor_vx_13(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
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

/* Instruction: vmax_vx_14 (OPIVX) */
/* Randomized vector max operation (OPIVX) */
val execute_vmax_vx_14 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vmax_vx_14(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
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

/* Instruction: vrem_vv_15 (OPIVV) */
/* Randomized vector rem operation (OPIVV) */
val execute_vrem_vv_15 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vrem_vv_15(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = (op2 % op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vxor_vx_16 (OPIVX) */
/* Randomized vector xor operation (OPIVX) */
val execute_vxor_vx_16 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vxor_vx_16(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
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

/* Instruction: vdiv_vv_17 (OPIVV) */
/* Randomized vector div operation (OPIVV) */
val execute_vdiv_vv_17 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vdiv_vv_17(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = (op2 / op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vabs_m_18 (OPMVV) */
/* Randomized unary vector abs operation */
val execute_vabs_m_18 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vabs_m_18(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = abs(op2);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vxor_vv_19 (OPIVV) */
/* Randomized vector xor operation (OPIVV) */
val execute_vxor_vv_19 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vxor_vv_19(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = (op2 ^ op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vclz_m_20 (OPMVV) */
/* Randomized unary vector clz operation */
val execute_vclz_m_20 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vclz_m_20(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = clz(op2);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vnot_m_21 (OPMVV) */
/* Randomized unary vector not operation */
val execute_vnot_m_21 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vnot_m_21(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = (~op2);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vmin_vv_22 (OPIVV) */
/* Randomized vector min operation (OPIVV) */
val execute_vmin_vv_22 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vmin_vv_22(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = min(op2, op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vcpop_m_23 (OPMVV) */
/* Randomized unary vector cpop operation */
val execute_vcpop_m_23 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vcpop_m_23(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = cpop(op2);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vor_vx_24 (OPIVX) */
/* Randomized vector or operation (OPIVX) */
val execute_vor_vx_24 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vor_vx_24(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
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

/* Instruction: vmul_vv_25 (OPIVV) */
/* Randomized vector mul operation (OPIVV) */
val execute_vmul_vv_25 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vmul_vv_25(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = (op2 * op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vcpop_m_26 (OPMVV) */
/* Randomized unary vector cpop operation */
val execute_vcpop_m_26 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vcpop_m_26(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = cpop(op2);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vdiv_vx_27 (OPIVX) */
/* Randomized vector div operation (OPIVX) */
val execute_vdiv_vx_27 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vdiv_vx_27(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
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

/* Instruction: vclz_m_28 (OPMVV) */
/* Randomized unary vector clz operation */
val execute_vclz_m_28 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vclz_m_28(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = clz(op2);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vsrl_vx_29 (OPIVX) */
/* Randomized vector srl operation (OPIVX) */
val execute_vsrl_vx_29 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vsrl_vx_29(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
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

/* Instruction: vsadd_vv_30 (OPIVV) */
/* Randomized vector sadd operation (OPIVV) */
val execute_vsadd_vv_30 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vsadd_vv_30(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let op1 = get_velem(vs1, i, 32);
      let res_elem = (op2 +_sat op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}

/* Instruction: vadd_vx_31 (OPIVX) */
/* Randomized vector add operation (OPIVX) */
val execute_vadd_vx_31 : (bits(5), bits(5), bits(5), bits(1)) -> unit
function execute_vadd_vx_31(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
  foreach (i from 0 to (vl - 1)) {
    if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
      let op2 = get_velem(vs2, i, 32);
      let rs1_val = rX(vs1_or_imm);
      let op1 = rs1_val;
      let res_elem = (op2 + op1);
      set_velem(vd, i, 32, res_elem);
    }
  };
}
