/******************************************************
 * SystemC Main Entrypoint for ArchC parsed_archc_isa model  *
 * Generated automatically by random_vISA             *
 ******************************************************/

const char *project_name = "parsed_archc_isa";
const char *project_file = "parsed_archc_isa.ac";
const char *archc_version = "2.4.1";
const char *archc_options = "";

#include <iostream>
#include <fstream>
#include <string>
#include <systemc.h>
#include "ac_stats_base.H"
#include "parsed_archc_isa.H"

static inline void write_word(parsed_archc_isa &proc, uint32_t addr, uint32_t val) {
    ac_ptr ptr(&val);
    proc.DM.write(ptr, addr, 32);
}

int sc_main(int ac, char *av[]) {
    std::cout << "============================================================" << std::endl;
    std::cout << "ArchC SystemC Simulator for parsed_archc_isa" << std::endl;
    std::cout << "WordSize = 32 bits, Num Vector Regs = 32" << std::endl;
    std::cout << "============================================================" << std::endl;

    parsed_archc_isa proc1("parsed_archc_isa");

    bool has_app = false;
    std::string bin_path = "";
    for (int i = 1; i < ac; ++i) {
        std::string arg = av[i];
        if (arg.find("--load=") == 0) {
            has_app = true;
            break;
        } else if (arg == "--" && i + 1 < ac) {
            has_app = true;
            break;
        } else if (arg.find("--bin=") == 0) {
            bin_path = arg.substr(6);
        } else if (arg == "--bin" && i + 1 < ac) {
            bin_path = av[++i];
        }
    }

    if (has_app) {
        proc1.init(ac, av);
        proc1.set_prog_args();
    } else {
        std::cout << "\n[ArchC] Initializing SystemC Vector Processing Core..." << std::endl;
        proc1.init();
        proc1.dec_cache_size = 65536;
        proc1.init_dec_cache();

        // Setup test register values
        proc1.VRB.write(1, 10);
        proc1.VRB.write(2, 2);
        proc1.XRB.write(1, 5);
        std::cout << "  State initialized: VRB[1] = 10, VRB[2] = 2, XRB[1] = 5" << std::endl;

        if (!bin_path.empty()) {
            std::ifstream bf(bin_path, std::ios::binary);
            if (bf.is_open()) {
                uint32_t word = 0;
                uint32_t addr = 0;
                while (bf.read(reinterpret_cast<char*>(&word), 4)) {
                    write_word(proc1, addr, word);
                    addr += 4;
                }
                std::cout << "  Loaded " << (addr / 4) << " bytecode instructions from " << bin_path << std::endl;
            }
        } else {
            // Load test sequence into DM
            uint32_t addr = 0;
            // Instruction vand_vv_0
            uint32_t w0 = ((0 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (0 << 12) | ((0 + 4) << 7) | 0x57;
            write_word(proc1, addr, w0);
            addr += 4;
            // Instruction vmax_vx_1
            uint32_t w1 = ((1 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (4 << 12) | ((1 + 4) << 7) | 0x57;
            write_word(proc1, addr, w1);
            addr += 4;
            // Instruction vdiv_vx_2
            uint32_t w2 = ((2 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (4 << 12) | ((2 + 4) << 7) | 0x57;
            write_word(proc1, addr, w2);
            addr += 4;
            // Instruction vxor_vx_3
            uint32_t w3 = ((3 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (4 << 12) | ((3 + 4) << 7) | 0x57;
            write_word(proc1, addr, w3);
            addr += 4;
            // Instruction vdiv_vx_4
            uint32_t w4 = ((4 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (4 << 12) | ((4 + 4) << 7) | 0x57;
            write_word(proc1, addr, w4);
            addr += 4;
            // Instruction vmax_vv_5
            uint32_t w5 = ((5 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (0 << 12) | ((5 + 4) << 7) | 0x57;
            write_word(proc1, addr, w5);
            addr += 4;
            // Instruction vdiv_vx_6
            uint32_t w6 = ((6 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (4 << 12) | ((6 + 4) << 7) | 0x57;
            write_word(proc1, addr, w6);
            addr += 4;
            // Instruction vor_vx_7
            uint32_t w7 = ((7 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (4 << 12) | ((7 + 4) << 7) | 0x57;
            write_word(proc1, addr, w7);
            addr += 4;
            std::cout << "  Loaded " << (addr / 4) << " synthesized vector instructions into Memory DM." << std::endl;
        }

        proc1.set_ac_pc(0);
    }

    std::cout << "\n[ArchC] Starting SystemC Simulation Kernel (sc_start)..." << std::endl;
    sc_start();

    std::cout << "\n============================================================" << std::endl;
    std::cout << "[ArchC SystemC Register State Dump]:" << std::endl;
    for (int r = 0; r < 8; ++r) {
        std::cout << "  VRB[" << r << "] = " << proc1.VRB.read(r) << std::endl;
    }
    for (int r = 0; r < 4; ++r) {
        std::cout << "  XRB[" << r << "] = " << proc1.XRB.read(r) << std::endl;
    }
    std::cout << "============================================================" << std::endl;

    proc1.PrintStat();
    return 0;
}