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
        proc1.dec_cache_size = 1048576;
        proc1.init_dec_cache();

        // Zero-initialize all register banks
        for (int i = 0; i < 32; ++i) {
            proc1.VRB.write(i, 0);
        }
        for (int i = 0; i < 32; ++i) {
            proc1.XRB.write(i, 0);
        }

        // Setup test register values
        proc1.VRB.write(1, 10);
        proc1.VRB.write(2, 2);
        proc1.XRB.write(1, 5);
        std::cout << "  State initialized: VRB[1] = 10, VRB[2] = 2, XRB[1] = 5" << std::endl;

        // NOTE: Load base is 0x100 to avoid ArchC reserved syscall stubs at 0x00-0xFF
        // (ac_forbidden is mapped to 0x3C by ArchC, so programs must start above that)
        if (!bin_path.empty()) {
            std::ifstream bf(bin_path, std::ios::binary);
            if (bf.is_open()) {
                uint32_t word = 0;
                uint32_t addr = 0x100;
                uint32_t n = 0;
                while (bf.read(reinterpret_cast<char*>(&word), 4)) {
                    write_word(proc1, addr, word);
                    addr += 4;
                    n++;
                }
                std::cout << "  Loaded " << n << " bytecode instructions from " << bin_path
                          << " at base 0x100" << std::endl;
            }
        } else {
            // Load all synthesized test instructions into DM (base 0x100)
            uint32_t addr = 0x100;
            // Instruction vclz_m_0
            uint32_t w0 = ((0 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (2 << 12) | ((4) << 7) | 0x57;
            write_word(proc1, addr, w0);
            addr += 4;
            // Instruction vor_vi_1
            uint32_t w1 = ((1 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (5 << 15) | (3 << 12) | ((5) << 7) | 0x57;
            write_word(proc1, addr, w1);
            addr += 4;
            // Instruction vxor_vx_2
            uint32_t w2 = ((2 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (4 << 12) | ((6) << 7) | 0x57;
            write_word(proc1, addr, w2);
            addr += 4;
            // Instruction vmin_vx_3
            uint32_t w3 = ((3 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (4 << 12) | ((7) << 7) | 0x57;
            write_word(proc1, addr, w3);
            addr += 4;
            // Instruction vsadd_vx_4
            uint32_t w4 = ((4 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (4 << 12) | ((8) << 7) | 0x57;
            write_word(proc1, addr, w4);
            addr += 4;
            // Instruction vsra_vx_5
            uint32_t w5 = ((5 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (4 << 12) | ((9) << 7) | 0x57;
            write_word(proc1, addr, w5);
            addr += 4;
            // Instruction vrem_vx_6
            uint32_t w6 = ((6 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (4 << 12) | ((10) << 7) | 0x57;
            write_word(proc1, addr, w6);
            addr += 4;
            // Instruction vabs_m_7
            uint32_t w7 = ((7 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (2 << 12) | ((11) << 7) | 0x57;
            write_word(proc1, addr, w7);
            addr += 4;
            // Instruction vclz_m_8
            uint32_t w8 = ((8 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (2 << 12) | ((12) << 7) | 0x57;
            write_word(proc1, addr, w8);
            addr += 4;
            // Instruction vsrl_vx_9
            uint32_t w9 = ((9 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (4 << 12) | ((13) << 7) | 0x57;
            write_word(proc1, addr, w9);
            addr += 4;
            // Instruction vcpop_m_10
            uint32_t w10 = ((10 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (2 << 12) | ((14) << 7) | 0x57;
            write_word(proc1, addr, w10);
            addr += 4;
            // Instruction vcpop_m_11
            uint32_t w11 = ((11 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (2 << 12) | ((15) << 7) | 0x57;
            write_word(proc1, addr, w11);
            addr += 4;
            // Instruction vrem_vv_12
            uint32_t w12 = ((12 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (0 << 12) | ((16) << 7) | 0x57;
            write_word(proc1, addr, w12);
            addr += 4;
            // Instruction vxor_vx_13
            uint32_t w13 = ((13 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (4 << 12) | ((17) << 7) | 0x57;
            write_word(proc1, addr, w13);
            addr += 4;
            // Instruction vmax_vx_14
            uint32_t w14 = ((14 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (4 << 12) | ((18) << 7) | 0x57;
            write_word(proc1, addr, w14);
            addr += 4;
            // Instruction vrem_vv_15
            uint32_t w15 = ((15 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (0 << 12) | ((19) << 7) | 0x57;
            write_word(proc1, addr, w15);
            addr += 4;
            // Instruction vxor_vx_16
            uint32_t w16 = ((16 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (4 << 12) | ((20) << 7) | 0x57;
            write_word(proc1, addr, w16);
            addr += 4;
            // Instruction vdiv_vv_17
            uint32_t w17 = ((17 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (0 << 12) | ((21) << 7) | 0x57;
            write_word(proc1, addr, w17);
            addr += 4;
            // Instruction vabs_m_18
            uint32_t w18 = ((18 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (2 << 12) | ((22) << 7) | 0x57;
            write_word(proc1, addr, w18);
            addr += 4;
            // Instruction vxor_vv_19
            uint32_t w19 = ((19 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (0 << 12) | ((23) << 7) | 0x57;
            write_word(proc1, addr, w19);
            addr += 4;
            // Instruction vclz_m_20
            uint32_t w20 = ((20 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (2 << 12) | ((24) << 7) | 0x57;
            write_word(proc1, addr, w20);
            addr += 4;
            // Instruction vnot_m_21
            uint32_t w21 = ((21 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (2 << 12) | ((25) << 7) | 0x57;
            write_word(proc1, addr, w21);
            addr += 4;
            // Instruction vmin_vv_22
            uint32_t w22 = ((22 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (0 << 12) | ((26) << 7) | 0x57;
            write_word(proc1, addr, w22);
            addr += 4;
            // Instruction vcpop_m_23
            uint32_t w23 = ((23 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (2 << 12) | ((27) << 7) | 0x57;
            write_word(proc1, addr, w23);
            addr += 4;
            // Instruction vor_vx_24
            uint32_t w24 = ((24 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (4 << 12) | ((28) << 7) | 0x57;
            write_word(proc1, addr, w24);
            addr += 4;
            // Instruction vmul_vv_25
            uint32_t w25 = ((25 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (0 << 12) | ((29) << 7) | 0x57;
            write_word(proc1, addr, w25);
            addr += 4;
            // Instruction vcpop_m_26
            uint32_t w26 = ((26 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (2 << 12) | ((30) << 7) | 0x57;
            write_word(proc1, addr, w26);
            addr += 4;
            // Instruction vdiv_vx_27
            uint32_t w27 = ((27 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (4 << 12) | ((31) << 7) | 0x57;
            write_word(proc1, addr, w27);
            addr += 4;
            // Instruction vclz_m_28
            uint32_t w28 = ((28 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (2 << 12) | ((4) << 7) | 0x57;
            write_word(proc1, addr, w28);
            addr += 4;
            // Instruction vsrl_vx_29
            uint32_t w29 = ((29 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (4 << 12) | ((5) << 7) | 0x57;
            write_word(proc1, addr, w29);
            addr += 4;
            // Instruction vsadd_vv_30
            uint32_t w30 = ((30 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (0 << 12) | ((6) << 7) | 0x57;
            write_word(proc1, addr, w30);
            addr += 4;
            // Instruction vadd_vx_31
            uint32_t w31 = ((31 & 0x3F) << 26) | (1 << 25) | (2 << 20) | (1 << 15) | (4 << 12) | ((7) << 7) | 0x57;
            write_word(proc1, addr, w31);
            addr += 4;
            // Append halt sentinel
            write_word(proc1, addr, 0);
            addr += 4;
            std::cout << "  Loaded " << ((addr - 0x100) / 4 - 1) << " synthesized vector instructions into Memory DM." << std::endl;
        }

        proc1.set_ac_pc(0x100);
    }

    std::cout << "\n[ArchC] Starting SystemC Simulation Kernel (sc_start)..." << std::endl;
    sc_start();

    std::cout << "\n============================================================" << std::endl;
    std::cout << "[ArchC SystemC Register State Dump]:" << std::endl;
    for (int r = 0; r < 32; ++r) {
        int32_t val = static_cast<int32_t>(proc1.VRB.read(r));
        if (val != 0 || r <= 2)
            std::cout << "  VRB[" << r << "] = " << val << std::endl;
    }
    for (int r = 0; r < 4; ++r) {
        std::cout << "  XRB[" << r << "] = " << proc1.XRB.read(r) << std::endl;
    }
    std::cout << "============================================================" << std::endl;

    proc1.PrintStat();
    return 0;
}