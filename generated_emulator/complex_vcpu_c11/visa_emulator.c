#include "visa_emulator.h"

void visa_emulator_init(EmulatorState* state) {
    memset(state, 0, sizeof(EmulatorState));
    state->csr.vl = VISA_VLEN / 32;
    state->csr.pc = 0x80000000;
}

void visa_emulator_reset(EmulatorState* state) {
    visa_emulator_init(state);
}

uint64_t visa_get_xreg(const EmulatorState* state, size_t idx) {
    if (idx == 0 || idx >= VISA_NUM_XREGS) return 0;
    return state->xregs[idx];
}

void visa_set_xreg(EmulatorState* state, size_t idx, uint64_t val) {
    if (idx > 0 && idx < VISA_NUM_XREGS) {
        state->xregs[idx] = val;
    }
}

bool visa_is_mask_set(const EmulatorState* state, size_t mask_reg, size_t elem_idx) {
    if (mask_reg >= VISA_NUM_VREGS) return false;
    size_t byte_idx = elem_idx / 8;
    size_t bit_idx = elem_idx % 8;
    if (byte_idx >= VISA_VLEN_BYTES) return false;
    return (state->vregs.regs[mask_reg][byte_idx] & (1 << bit_idx)) != 0;
}

void visa_dump_vregs(const EmulatorState* state) {
    for (size_t i = 0; i < VISA_NUM_VREGS; ++i) {
        printf("v%02zu: [ ", i);
        for (int b = (int)VISA_VLEN_BYTES - 1; b >= 0; --b) {
            printf("%02x ", state->vregs.regs[i][b]);
        }
        printf("]\n");
    }
}

DecodedInstruction visa_decode(uint32_t word) {
    DecodedInstruction dec;
    memset(&dec, 0, sizeof(DecodedInstruction));
    dec.raw_word = word;
    dec.opcode = word & 0x7F;
    dec.vd = (word >> 7) & 0x1F;
    dec.funct3 = (word >> 12) & 0x7;
    dec.vs1 = (word >> 15) & 0x1F;
    dec.rs1 = dec.vs1;
    int32_t imm5 = (int32_t)((word >> 15) & 0x1F);
    if (imm5 & 0x10) imm5 |= ~0x1F;
    dec.imm = (int8_t)imm5;
    dec.vs2 = (word >> 20) & 0x1F;
    dec.vm = (word >> 25) & 0x1;
    dec.funct6 = (word >> 26) & 0x3F;
    dec.mnemonic = "unknown";

    switch (dec.funct6) {
    case 0:
        if (dec.funct3 == 2) {
            dec.mnemonic = "vclz_m_0";
        }
        break;
    case 1:
        if (dec.funct3 == 3) {
            dec.mnemonic = "vor_vi_1";
        }
        break;
    case 2:
        if (dec.funct3 == 4) {
            dec.mnemonic = "vxor_vx_2";
        }
        break;
    case 3:
        if (dec.funct3 == 4) {
            dec.mnemonic = "vmin_vx_3";
        }
        break;
    case 4:
        if (dec.funct3 == 4) {
            dec.mnemonic = "vsadd_vx_4";
        }
        break;
    case 5:
        if (dec.funct3 == 4) {
            dec.mnemonic = "vsra_vx_5";
        }
        break;
    case 6:
        if (dec.funct3 == 4) {
            dec.mnemonic = "vrem_vx_6";
        }
        break;
    case 7:
        if (dec.funct3 == 2) {
            dec.mnemonic = "vabs_m_7";
        }
        break;
    case 8:
        if (dec.funct3 == 2) {
            dec.mnemonic = "vclz_m_8";
        }
        break;
    case 9:
        if (dec.funct3 == 4) {
            dec.mnemonic = "vsrl_vx_9";
        }
        break;
    case 10:
        if (dec.funct3 == 2) {
            dec.mnemonic = "vcpop_m_10";
        }
        break;
    case 11:
        if (dec.funct3 == 2) {
            dec.mnemonic = "vcpop_m_11";
        }
        break;
    case 12:
        if (dec.funct3 == 0) {
            dec.mnemonic = "vrem_vv_12";
        }
        break;
    case 13:
        if (dec.funct3 == 4) {
            dec.mnemonic = "vxor_vx_13";
        }
        break;
    case 14:
        if (dec.funct3 == 4) {
            dec.mnemonic = "vmax_vx_14";
        }
        break;
    case 15:
        if (dec.funct3 == 0) {
            dec.mnemonic = "vrem_vv_15";
        }
        break;
    case 16:
        if (dec.funct3 == 4) {
            dec.mnemonic = "vxor_vx_16";
        }
        break;
    case 17:
        if (dec.funct3 == 0) {
            dec.mnemonic = "vdiv_vv_17";
        }
        break;
    case 18:
        if (dec.funct3 == 2) {
            dec.mnemonic = "vabs_m_18";
        }
        break;
    case 19:
        if (dec.funct3 == 0) {
            dec.mnemonic = "vxor_vv_19";
        }
        break;
    case 20:
        if (dec.funct3 == 2) {
            dec.mnemonic = "vclz_m_20";
        }
        break;
    case 21:
        if (dec.funct3 == 2) {
            dec.mnemonic = "vnot_m_21";
        }
        break;
    case 22:
        if (dec.funct3 == 0) {
            dec.mnemonic = "vmin_vv_22";
        }
        break;
    case 23:
        if (dec.funct3 == 2) {
            dec.mnemonic = "vcpop_m_23";
        }
        break;
    case 24:
        if (dec.funct3 == 4) {
            dec.mnemonic = "vor_vx_24";
        }
        break;
    case 25:
        if (dec.funct3 == 0) {
            dec.mnemonic = "vmul_vv_25";
        }
        break;
    case 26:
        if (dec.funct3 == 2) {
            dec.mnemonic = "vcpop_m_26";
        }
        break;
    case 27:
        if (dec.funct3 == 4) {
            dec.mnemonic = "vdiv_vx_27";
        }
        break;
    case 28:
        if (dec.funct3 == 2) {
            dec.mnemonic = "vclz_m_28";
        }
        break;
    case 29:
        if (dec.funct3 == 4) {
            dec.mnemonic = "vsrl_vx_29";
        }
        break;
    case 30:
        if (dec.funct3 == 0) {
            dec.mnemonic = "vsadd_vv_30";
        }
        break;
    case 31:
        if (dec.funct3 == 4) {
            dec.mnemonic = "vadd_vx_31";
        }
        break;
    default:
        break;
    }
    return dec;
}

bool visa_step(EmulatorState* state, uint32_t word) {
    DecodedInstruction dec = visa_decode(word);
    if (dec.opcode != 0x57) return false;
    return visa_execute(state, &dec);
}

size_t visa_run_program(EmulatorState* state, const uint32_t* program, size_t count) {
    size_t executed = 0;
    for (size_t i = 0; i < count; ++i) {
        if (!visa_step(state, program[i])) break;
        executed++;
        state->csr.pc += 4;
    }
    return executed;
}