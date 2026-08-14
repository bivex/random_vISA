"""Unit tests for ANTLR4 Sail Specification Parser."""

import pytest
from random_visa.adapters.inbound.parser.sail_antlr_adapter import AntlrSailParserAdapter
from random_visa.domain.model.types import InstructionFormat, BinaryOp, UnaryOp


def test_parse_sail_snippet():
    sail_code = """
    default Order dec
    $include <prelude.sail>

    let VLEN : int = 256
    let ELEN : int = 64
    let NUM_VREGS : int = 32

    type vreg_idx = range(0, 31)
    type vreg_t = bits(VLEN)

    register v0 : vreg_t
    register vl : bits(64)

    val execute_vadd_vv_0 : (bits(5), bits(5), bits(5), bits(1)) -> unit
    function execute_vadd_vv_0(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
      foreach (i from 0 to (vl - 1)) {
        if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
          let op2 = get_velem(vs2, i, 32);
          let op1 = get_velem(vs1, i, 32);
          let res_elem = (op2 + op1);
          set_velem(vd, i, 32, res_elem);
        }
      };
    }

    val execute_vclz_m_1 : (bits(5), bits(5), bits(5), bits(1)) -> unit
    function execute_vclz_m_1(vd_idx: bits(5), vs2_idx: bits(5), vs1_or_imm: bits(5), vm: bits(1)) = {
      foreach (i from 0 to (vl - 1)) {
        if (vm == 1 | get_vmask_bit(v0, i) == 1) then {
          let op2 = get_velem(vs2, i, 32);
          let res_elem = clz(op2);
          set_velem(vd, i, 32, res_elem);
        }
      };
    }
    """

    parser = AntlrSailParserAdapter()
    spec = parser.parse_sail_source(sail_code, spec_name="TestSailSpec")

    assert spec.name == "TestSailSpec"
    assert spec.config.vlen == 256
    assert spec.config.elen == 64
    assert len(spec.instructions) == 2

    inst1 = spec.instructions[0]
    assert inst1.mnemonic == "vadd_vv_0"
    assert inst1.format == InstructionFormat.OP_VV
    assert inst1.binary_op == BinaryOp.ADD

    inst2 = spec.instructions[1]
    assert inst2.mnemonic == "vclz_m_1"
    assert inst2.format == InstructionFormat.OP_MVV
    assert inst2.unary_op == UnaryOp.CLZ
