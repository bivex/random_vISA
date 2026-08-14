#include "emulator.hpp"
#include "decoder.hpp"
#include <iostream>
#include <vector>
#include <cassert>

using namespace visa_emulator;

int main() {
    std::cout << "============================================================\n";
    std::cout << "Starting Vector ISA (RVV_Custom_ISA) Emulator Verification Suite\n";
    std::cout << "VLEN = " << VLEN << " bits, Num VRegs = " << NUM_VREGS << "\n";
    std::cout << "============================================================\n";

    VectorEmulator emu;
    emu.reset();
    emu.state.csr.vl = 4; // Set vector length to 4 elements (32-bit each)

    // Pre-populate source registers v1 and v2 with test data
    for (size_t i = 0; i < 4; ++i) {
        emu.state.vregs.set_elem<int32_t>(1, i, static_cast<int32_t>((i + 1) * 10)); // v1 = [10, 20, 30, 40]
        emu.state.vregs.set_elem<int32_t>(2, i, static_cast<int32_t>((i + 1) * 2));  // v2 = [2, 4, 6, 8]
    }
    emu.state.set_xreg(1, 5); // x1 = 5

    std::cout << "[Initial Register State]\n";
    std::cout << "v1: ";
    for (size_t i = 0; i < 4; ++i) std::cout << emu.state.vregs.get_elem<int32_t>(1, i) << " ";
    std::cout << "\nv2: ";
    for (size_t i = 0; i < 4; ++i) std::cout << emu.state.vregs.get_elem<int32_t>(2, i) << " ";
    std::cout << "\nx1: " << emu.state.get_xreg(1) << "\n\n";

    // Test each synthesized instruction
    std::vector<uint32_t> test_words = {
        // vadd_vi_0 (funct6=0, funct3=3)
        0x0220B1D7u,
        // vand_vv_1 (funct6=1, funct3=0)
        0x062081D7u,
        // vmax_vv_2 (funct6=2, funct3=0)
        0x0A2081D7u,
        // vadd_vv_3 (funct6=3, funct3=0)
        0x0E2081D7u,
        // vnot_m_4 (funct6=4, funct3=2)
        0x1220A1D7u,
        // vsadd_vx_5 (funct6=5, funct3=4)
        0x1620C1D7u,
        // vctz_m_6 (funct6=6, funct3=2)
        0x1A20A1D7u,
        // vadd_vv_7 (funct6=7, funct3=0)
        0x1E2081D7u,
    };

    size_t passed = 0;
    for (size_t idx = 0; idx < test_words.size(); ++idx) {
        uint32_t word = test_words[idx];
        DecodedInstruction dec = Decoder::decode(word);
        std::cout << "[Test " << idx + 1 << "/" << test_words.size() << "] Executing "
                  << dec.mnemonic << " (0x" << std::hex << word << std::dec << ")... ";

        bool ok = emu.step(word);
        if (ok) {
            std::cout << "SUCCESS -> v3: [ ";
            for (size_t elem = 0; elem < 4; ++elem) {
                std::cout << emu.state.vregs.get_elem<int32_t>(3, elem) << " ";
            }
            std::cout << "]\n";
            passed++;
        } else {
            std::cout << "FAILED to decode/execute!\n";
        }
    }

    std::cout << "\n============================================================\n";
    std::cout << "Results: " << passed << "/" << test_words.size() << " instructions executed successfully.\n";
    std::cout << "============================================================\n";

    return (passed == test_words.size()) ? 0 : 1;
}