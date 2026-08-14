#include "emulator.hpp"
#include "decoder.hpp"
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <cassert>

using namespace visa_emulator;

void run_custom_bytecode(VectorEmulator& emu, const std::vector<uint32_t>& program) {
    std::cout << "Executing Bytecode Program (" << program.size() << " instructions)...\n";
    for (size_t idx = 0; idx < program.size(); ++idx) {
        uint32_t word = program[idx];
        DecodedInstruction dec = Decoder::decode(word);
        std::cout << "  [" << idx + 1 << "] PC=0x" << std::hex << emu.state.csr.pc
                  << " Word=0x" << word << " (" << dec.mnemonic << ")... " << std::dec;
        bool ok = emu.step(word);
        if (ok) {
            std::cout << "OK -> vd (v" << static_cast<int>(dec.vd) << "): [ ";
            for (size_t elem = 0; elem < static_cast<size_t>(emu.state.csr.vl); ++elem) {
                std::cout << emu.state.vregs.get_elem<int32_t>(dec.vd, elem) << " ";
            }
            std::cout << "]\n";
            emu.state.csr.pc += 4;
        } else {
            std::cout << "DECODE/EXECUTION FAILED!\n";
            return;
        }
    }

    std::cout << "\n[Final Vector Register File Dump]:\n";
    emu.state.vregs.dump(std::cout);
}

int main(int argc, char** argv) {
    VectorEmulator emu;
    emu.reset();
    emu.state.csr.vl = 4; // Set vector length to 4 elements (32-bit each)

    // Pre-populate source registers v1 and v2 with test data
    for (size_t i = 0; i < 4; ++i) {
        emu.state.vregs.set_elem<int32_t>(1, i, static_cast<int32_t>((i + 1) * 10)); // v1 = [10, 20, 30, 40]
        emu.state.vregs.set_elem<int32_t>(2, i, static_cast<int32_t>((i + 1) * 2));  // v2 = [2, 4, 6, 8]
    }
    emu.state.set_xreg(1, 5); // x1 = 5

    // Check for --bin <filename> argument
    if (argc >= 3 && std::string(argv[1]) == "--bin") {
        std::string filename = argv[2];
        std::ifstream file(filename, std::ios::binary);
        if (!file.is_open()) {
            std::cerr << "Error: cannot open binary bytecode file " << filename << "\n";
            return 1;
        }
        std::vector<uint32_t> program;
        uint32_t word;
        while (file.read(reinterpret_cast<char*>(&word), sizeof(uint32_t))) {
            program.push_back(word);
        }
        run_custom_bytecode(emu, program);
        return 0;
    }

    // Check for --hex <word1> <word2> ... argument
    if (argc >= 3 && std::string(argv[1]) == "--hex") {
        std::vector<uint32_t> program;
        for (int i = 2; i < argc; ++i) {
            uint32_t word = static_cast<uint32_t>(std::stoul(argv[i], nullptr, 0));
            program.push_back(word);
        }
        run_custom_bytecode(emu, program);
        return 0;
    }

    // Default verification suite
    std::cout << "============================================================\n";
    std::cout << "Starting Vector ISA (HyperVector_ISA) Emulator Verification Suite\n";
    std::cout << "VLEN = " << VLEN << " bits, Num VRegs = " << NUM_VREGS << "\n";
    std::cout << "============================================================\n";

    std::cout << "[Initial Register State]\n";
    std::cout << "v1: ";
    for (size_t i = 0; i < 4; ++i) std::cout << emu.state.vregs.get_elem<int32_t>(1, i) << " ";
    std::cout << "\nv2: ";
    for (size_t i = 0; i < 4; ++i) std::cout << emu.state.vregs.get_elem<int32_t>(2, i) << " ";
    std::cout << "\nx1: " << emu.state.get_xreg(1) << "\n\n";

    std::vector<uint32_t> test_words = {
        // vand_vv_0 (funct6=0, funct3=0)
        0x022081D7u,
        // vmax_vx_1 (funct6=1, funct3=4)
        0x0620C1D7u,
        // vdiv_vx_2 (funct6=2, funct3=4)
        0x0A20C1D7u,
        // vxor_vx_3 (funct6=3, funct3=4)
        0x0E20C1D7u,
        // vdiv_vx_4 (funct6=4, funct3=4)
        0x1220C1D7u,
        // vmax_vv_5 (funct6=5, funct3=0)
        0x162081D7u,
        // vdiv_vx_6 (funct6=6, funct3=4)
        0x1A20C1D7u,
        // vor_vx_7 (funct6=7, funct3=4)
        0x1E20C1D7u,
        // vsrl_vx_8 (funct6=8, funct3=4)
        0x2220C1D7u,
        // vclz_m_9 (funct6=9, funct3=2)
        0x2620A1D7u,
        // vmin_vx_10 (funct6=10, funct3=4)
        0x2A20C1D7u,
        // vmul_vv_11 (funct6=11, funct3=0)
        0x2E2081D7u,
        // vsrl_vv_12 (funct6=12, funct3=0)
        0x322081D7u,
        // vsadd_vx_13 (funct6=13, funct3=4)
        0x3620C1D7u,
        // vmul_vv_14 (funct6=14, funct3=0)
        0x3A2081D7u,
        // vmax_vx_15 (funct6=15, funct3=4)
        0x3E20C1D7u,
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