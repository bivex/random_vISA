#pragma once
#include <cstdint>
#include <string_view>
#include <optional>

namespace visa_emulator {

enum class InstId {
    UNKNOWN = 0,
    VAND_VV_0,
    VMAX_VX_1,
    VDIV_VX_2,
    VXOR_VX_3,
    VDIV_VX_4,
    VMAX_VV_5,
    VDIV_VX_6,
    VOR_VX_7,
    VSRL_VX_8,
    VCLZ_M_9,
    VMIN_VX_10,
    VMUL_VV_11,
    VSRL_VV_12,
    VSADD_VX_13,
    VMUL_VV_14,
    VMAX_VX_15,
};

struct DecodedInstruction {
    InstId id{InstId::UNKNOWN};
    std::string_view mnemonic{"unknown"};
    uint8_t opcode{0};
    uint8_t funct3{0};
    uint8_t funct6{0};
    uint8_t vd{0};
    uint8_t vs2{0};
    uint8_t vs1{0};
    uint8_t rs1{0};
    int8_t imm{0};
    uint8_t vm{1};
    uint32_t raw_word{0};
};

class Decoder {
public:
    static inline DecodedInstruction decode(uint32_t word) noexcept {
        DecodedInstruction dec;
        dec.raw_word = word;
        dec.opcode = word & 0x7F;
        dec.vd = (word >> 7) & 0x1F;
        dec.funct3 = (word >> 12) & 0x7;
        dec.vs1 = (word >> 15) & 0x1F;
        dec.rs1 = dec.vs1;
        int32_t imm5 = static_cast<int32_t>((word >> 15) & 0x1F);
        if (imm5 & 0x10) imm5 |= ~0x1F;
        dec.imm = static_cast<int8_t>(imm5);
        dec.vs2 = (word >> 20) & 0x1F;
        dec.vm = (word >> 25) & 0x1;
        dec.funct6 = (word >> 26) & 0x3F;

        if (dec.opcode != 0x57) {
            return dec;
        }

        switch (dec.funct6) {
        case 0:
            if (dec.funct3 == 0) {
                dec.id = InstId::VAND_VV_0;
                dec.mnemonic = "vand_vv_0";
                return dec;
            }
            break;
        case 1:
            if (dec.funct3 == 4) {
                dec.id = InstId::VMAX_VX_1;
                dec.mnemonic = "vmax_vx_1";
                return dec;
            }
            break;
        case 2:
            if (dec.funct3 == 4) {
                dec.id = InstId::VDIV_VX_2;
                dec.mnemonic = "vdiv_vx_2";
                return dec;
            }
            break;
        case 3:
            if (dec.funct3 == 4) {
                dec.id = InstId::VXOR_VX_3;
                dec.mnemonic = "vxor_vx_3";
                return dec;
            }
            break;
        case 4:
            if (dec.funct3 == 4) {
                dec.id = InstId::VDIV_VX_4;
                dec.mnemonic = "vdiv_vx_4";
                return dec;
            }
            break;
        case 5:
            if (dec.funct3 == 0) {
                dec.id = InstId::VMAX_VV_5;
                dec.mnemonic = "vmax_vv_5";
                return dec;
            }
            break;
        case 6:
            if (dec.funct3 == 4) {
                dec.id = InstId::VDIV_VX_6;
                dec.mnemonic = "vdiv_vx_6";
                return dec;
            }
            break;
        case 7:
            if (dec.funct3 == 4) {
                dec.id = InstId::VOR_VX_7;
                dec.mnemonic = "vor_vx_7";
                return dec;
            }
            break;
        case 8:
            if (dec.funct3 == 4) {
                dec.id = InstId::VSRL_VX_8;
                dec.mnemonic = "vsrl_vx_8";
                return dec;
            }
            break;
        case 9:
            if (dec.funct3 == 2) {
                dec.id = InstId::VCLZ_M_9;
                dec.mnemonic = "vclz_m_9";
                return dec;
            }
            break;
        case 10:
            if (dec.funct3 == 4) {
                dec.id = InstId::VMIN_VX_10;
                dec.mnemonic = "vmin_vx_10";
                return dec;
            }
            break;
        case 11:
            if (dec.funct3 == 0) {
                dec.id = InstId::VMUL_VV_11;
                dec.mnemonic = "vmul_vv_11";
                return dec;
            }
            break;
        case 12:
            if (dec.funct3 == 0) {
                dec.id = InstId::VSRL_VV_12;
                dec.mnemonic = "vsrl_vv_12";
                return dec;
            }
            break;
        case 13:
            if (dec.funct3 == 4) {
                dec.id = InstId::VSADD_VX_13;
                dec.mnemonic = "vsadd_vx_13";
                return dec;
            }
            break;
        case 14:
            if (dec.funct3 == 0) {
                dec.id = InstId::VMUL_VV_14;
                dec.mnemonic = "vmul_vv_14";
                return dec;
            }
            break;
        case 15:
            if (dec.funct3 == 4) {
                dec.id = InstId::VMAX_VX_15;
                dec.mnemonic = "vmax_vx_15";
                return dec;
            }
            break;
        default:
            break;
        }
        return dec;
    }
};

} // namespace visa_emulator