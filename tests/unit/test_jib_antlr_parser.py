"""Unit tests for Sail Jib IR ANTLR4 Parser."""

from antlr4 import InputStream, CommonTokenStream
from random_visa.adapters.inbound.parser.antlr.JibLexer import JibLexer
from random_visa.adapters.inbound.parser.antlr.JibParser import JibParser
from random_visa.adapters.inbound.parser.antlr.JibVisitor import JibVisitor


def test_parse_jib_ir_program():
    jib_code = """
    #pragma sail target c

    struct VRegState = {
        v0: bv(128),
        vl: i(64)
    }

    enum RoundingMode = {
        RNE,
        RTZ,
        RDN,
        RUP
    }

    register v0 : bv(128);
    register vl : i(64);

    val get_velem : (bv(128), i(64)) -> i(32);

    fn execute_vadd_vv(vd: bv(5), vs2: bv(5), vs1: bv(5), vm: bit) -> unit {
        var %i : i(64);
        var %op2 : i(32);
        var %op1 : i(32);
        var %res : i(32);
        var %cond : bool;

        %i = 0;
    label loop_head:
        %cond = %i < vl;
        jump_if %cond loop_body;
        goto loop_end;

    label loop_body:
        %op2 = call get_velem(vs2, %i);
        %op1 = call get_velem(vs1, %i);
        %res = %op2 + %op1;
        call set_velem(vd, %i, %res);
        %i = %i + 1;
        goto loop_head;

    label loop_end:
        return ();
    }
    """

    input_stream = InputStream(jib_code)
    lexer = JibLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = JibParser(tokens)

    tree = parser.spec()

    assert parser.getNumberOfSyntaxErrors() == 0
    assert tree is not None
    assert len(tree.topLevelItem()) == 7
