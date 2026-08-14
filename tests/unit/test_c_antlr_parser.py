"""Unit tests for ISO C11/C99 ANTLR4 Parser Adapter."""

from random_visa.adapters.inbound.parser.c_antlr_adapter import AntlrCParserAdapter


def test_parse_c_source_functions_and_structs():
    c_source = """
    typedef struct {
        uint64_t vl;
        uint64_t pc;
    } CSRState;

    struct VRegState {
        uint8_t regs[32][16];
    };

    int32_t execute_vadd_vv(int32_t a, int32_t b) {
        return a + b;
    }

    void visa_step(CSRState* state) {
        state->pc += 4;
    }
    """

    res = AntlrCParserAdapter.parse_c_source(c_source)
    assert res["syntax_errors"] == 0
    assert "execute_vadd_vv" in res["functions"]
    assert "visa_step" in res["functions"]
    assert "VRegState" in res["structs"]
