#pragma once
#include <cstdint>
#include <string_view>
#include <optional>

namespace visa_emulator {

enum class InstId {
    UNKNOWN = 0,
    VADD_VI_0,
    VAND_VV_1,
    VMAX_VV_2,
    VADD_VV_3,
    VNOT_M_4,
    VSADD_VX_5,
    VCTZ_M_6,
    VADD_VV_7,
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
    static DecodedInstruction decode(uint32_t word) {
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
            if (dec.funct3 == 3) {
                dec.id = InstId::VADD_VI_0;
                dec.mnemonic = "vadd_vi_0";
                return dec;
            }
            break;
        case 1:
            if (dec.funct3 == 0) {
                dec.id = InstId::VAND_VV_1;
                dec.mnemonic = "vand_vv_1";
                return dec;
            }
            break;
        case 2:
            if (dec.funct3 == 0) {
                dec.id = InstId::VMAX_VV_2;
                dec.mnemonic = "vmax_vv_2";
                return dec;
            }
            break;
        case 3:
            if (dec.funct3 == 0) {
                dec.id = InstId::VADD_VV_3;
                dec.mnemonic = "vadd_vv_3";
                return dec;
            }
            break;
        case 4:
            if (dec.funct3 == 2) {
                dec.id = InstId::VNOT_M_4;
                dec.mnemonic = "vnot_m_4";
                return dec;
            }
            break;
        case 5:
            if (dec.funct3 == 4) {
                dec.id = InstId::VSADD_VX_5;
                dec.mnemonic = "vsadd_vx_5";
                return dec;
            }
            break;
        case 6:
            if (dec.funct3 == 2) {
                dec.id = InstId::VCTZ_M_6;
                dec.mnemonic = "vctz_m_6";
                return dec;
            }
            break;
        case 7:
            if (dec.funct3 == 0) {
                dec.id = InstId::VADD_VV_7;
                dec.mnemonic = "vadd_vv_7";
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