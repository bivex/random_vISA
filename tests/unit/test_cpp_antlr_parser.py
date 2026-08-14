"""Unit tests for ISO C++14 ANTLR4 Parser Adapter."""

from random_visa.adapters.inbound.parser.cpp_antlr_adapter import AntlrCppParserAdapter


def test_parse_cpp14_source():
    cpp_source = """
    #pragma once
    #include <cstdint>

    namespace visa_emulator {

    class VRegFile {
    public:
        alignas(64) uint8_t regs[32][16];

        void reset() noexcept {
            for (int i = 0; i < 32; ++i) {
                // reset
            }
        }
    };

    struct EmulatorState {
        VRegFile vregs;
        uint64_t xregs[32];
    };

    class InstructionExecutor {
    public:
        static bool execute(EmulatorState& state, uint32_t word) noexcept;
    };

    } // namespace visa_emulator
    """

    res = AntlrCppParserAdapter.parse_cpp_source(cpp_source)
    assert res["syntax_errors"] == 0
    assert "VRegFile" in res["classes"]
    assert "EmulatorState" in res["classes"]
    assert "InstructionExecutor" in res["classes"]
    assert "visa_emulator" in res["namespaces"]
