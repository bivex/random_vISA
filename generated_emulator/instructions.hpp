#pragma once
#include "isa_state.hpp"
#include "decoder.hpp"

namespace visa_emulator {

class InstructionExecutor {
public:
    static bool execute(EmulatorState& state, const DecodedInstruction& inst);

private:
    static void exec_vadd_vi_0(EmulatorState& state, const DecodedInstruction& inst);
    static void exec_vand_vv_1(EmulatorState& state, const DecodedInstruction& inst);
    static void exec_vmax_vv_2(EmulatorState& state, const DecodedInstruction& inst);
    static void exec_vadd_vv_3(EmulatorState& state, const DecodedInstruction& inst);
    static void exec_vnot_m_4(EmulatorState& state, const DecodedInstruction& inst);
    static void exec_vsadd_vx_5(EmulatorState& state, const DecodedInstruction& inst);
    static void exec_vctz_m_6(EmulatorState& state, const DecodedInstruction& inst);
    static void exec_vadd_vv_7(EmulatorState& state, const DecodedInstruction& inst);
};

} // namespace visa_emulator